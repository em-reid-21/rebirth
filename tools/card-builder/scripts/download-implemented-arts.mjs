/**
 * Downloads images from data for all implemented cards
 *
 * Usage (from tools/card-builder):
 *   npm run download:arts
 */
import { createWriteStream, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { pipeline } from 'node:stream/promises';
import { fileURLToPath } from 'node:url';
import { cleanName, spiritSetCodeFromCatalogId } from './set-mapping.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');
const repoRoot = join(rootDir, '../..');
const cardsDir = join(rootDir, 'data/pokemon-tcg-data/cards/en');
const jpCardsDir = join(rootDir, 'data/limitless-jp/cards');
const artsRoot = join(repoRoot, 'spirit/assets/cards');

const CONCURRENCY = 8;

const JP_SET_MAP = {
    ME6: 'M6',
};

// SVE energy as base, Sun/Moon energy for Fairy
const FREE_ENERGY_CARD_IDS = {
    GrassEnergy: 'sve-1',
    FireEnergy: 'sve-2',
    WaterEnergy: 'sve-3',
    LightningEnergy: 'sve-4',
    PsychicEnergy: 'sve-5',
    FightingEnergy: 'sve-6',
    DarknessEnergy: 'sve-7',
    MetalEnergy: 'sve-8',
    FairyEnergy: 'sm1-172',
};

function getImplementedCardIds() {
    const path = join(rootDir, 'implementedCardIds.json');

    if (!existsSync(path)) {
        console.error(`Missing ${path}`);
        console.error('Run: npm run generate:implemented-ids');
        process.exit(1);
    }

    return JSON.parse(readFileSync(path, 'utf8')).implementedCardIds;
}

function getCard(cardId) {
    const setId = cardId.slice(0, cardId.indexOf('-'));
    const setFile = join(cardsDir, `${setId}.json`);

    if (!existsSync(setFile)) return null;

    const cards = JSON.parse(readFileSync(setFile, 'utf8'));
    return cards.find(card => card.id === cardId) ?? null;
}

function loadLimitlessCards(limitlessId) {
    const cacheFile = join(jpCardsDir, `${limitlessId}.json`);

    if (!existsSync(cacheFile)) return null;

    return JSON.parse(readFileSync(cacheFile, 'utf8')).cards;
}

function artPath(card, spiritCode) {
    const name = cleanName(card.name);
    const num = parseInt(card.number, 10);

    return join(artsRoot, spiritCode, `${name}_${num}.png`);
}

async function downloadFile(url, dest) {
    const res = await fetch(url);

    if (!res.ok) {
        throw new Error(`HTTP ${res.status} for ${url}`);
    }

    mkdirSync(dirname(dest), { recursive: true });
    await pipeline(res.body, createWriteStream(dest));
}

async function runPool(tasks, concurrency) {
    const iter = tasks[Symbol.iterator]();
    let active = 0;
    let done = 0;

    return new Promise((resolve, reject) => {
        function next() {
            while (active < concurrency) {
                const { value: task, done: finished } = iter.next();

                if (finished) {
                    if (active === 0) resolve(done);
                    return;
                }

                active++;

                task()
                    .then(() => {
                        active--;
                        done++;
                        next();
                    })
                    .catch(reject);
            }
        }

        next();
    });
}

async function handleFreeEnergy(stats, ids) {
    if (!ids.length) return;

    const scriptsDir = join(repoRoot, 'spirit/game/scripts/cards/Free_Energy');
    const nameByNumber = new Map();

    if (existsSync(scriptsDir)) {
        for (const file of readdirSync(scriptsDir)) {
            if (!file.endsWith('.py')) continue;

            const name = file.slice(0, -3);
            const separator = name.lastIndexOf('_');

            if (separator === -1) continue;

            const cardName = name.slice(0, separator);
            const number = parseInt(name.slice(separator + 1), 10);

            if (!Number.isNaN(number)) {
                nameByNumber.set(number, cardName);
            }
        }
    }

    const outDir = join(artsRoot, 'Free_Energy');

    for (const id of ids) {
        const num = parseInt(id.split('-').pop(), 10);
        const name = nameByNumber.get(num);

        if (!name) {
            stats.skippedNoData++;
            continue;
        }

        const dest = join(outDir, `${name}_${num}.png`);

        if (existsSync(dest)) {
            stats.skippedExisting++;
            continue;
        }

        const tcgId = FREE_ENERGY_CARD_IDS[name];

        if (!tcgId) {
            console.warn(`Free_Energy: no mapping for "${name}", skipping`);
            stats.skippedNoData++;
            continue;
        }

        const card = getCard(tcgId);

        if (!card) {
            console.warn(`Free_Energy: card data missing for ${tcgId}, skipping`);
            stats.skippedNoData++;
            continue;
        }

        try {
            mkdirSync(outDir, { recursive: true });
            await downloadFile(card.images.large, dest);

            stats.downloaded++;
            console.log(`downloaded Free_Energy/${name}_${num}.png (${tcgId})`);
        } catch (err) {
            stats.failed++;
            console.error(`failed ${id}: ${err.message}`);
        }
    }
}

async function handleJpSet(spiritCode, limitlessId, stats, ids) {
    if (!ids.length) return;

    const cards = loadLimitlessCards(limitlessId);

    if (!cards) {
        console.warn(
            `${spiritCode}: no Limitless cache for ${limitlessId} — ` +
            `run: npm run sync-data:jp -- --sets ${limitlessId}`
        );

        stats.skippedNoData += ids.length;
        return;
    }

    const byNumber = new Map(
        cards.map(card => [parseInt(card.localId, 10), card])
    );

    const outDir = join(artsRoot, spiritCode);

    for (const id of ids) {
        const num = parseInt(id.split('-').pop(), 10);
        const card = byNumber.get(num);

        if (!card) {
            console.warn(`${spiritCode}: no Limitless card for number ${num}`);
            stats.skippedNoData++;
            continue;
        }

        const dest = join(
            outDir,
            `${cleanName(card.name)}_${num}.png`
        );

        if (existsSync(dest)) {
            stats.skippedExisting++;
            continue;
        }

        try {
            mkdirSync(outDir, { recursive: true });
            await downloadFile(card.image, dest);

            stats.downloaded++;
            console.log(
                `downloaded ${spiritCode}/${cleanName(card.name)}_${num}.png ` +
                `(${limitlessId}-${card.localId})`
            );
        } catch (err) {
            stats.failed++;
            console.error(`failed ${id}: ${err.message}`);
        }
    }
}

async function main() {
    const allIds = getImplementedCardIds();

    console.log(`Processing ${allIds.length} implemented card IDs…`);

    const jpPrefixToCode = Object.fromEntries(
        Object.keys(JP_SET_MAP).map(code => [code.toLowerCase(), code])
    );

    const normalIds = [];
    const freeEnergyIds = [];
    const jpIdsByCode = Object.fromEntries(
        Object.keys(JP_SET_MAP).map(code => [code, []])
    );

    for (const id of allIds) {
        const prefix = id.slice(0, id.indexOf('-'));

        if (prefix === 'free_energy') {
            freeEnergyIds.push(id);
        } else if (jpPrefixToCode[prefix]) {
            jpIdsByCode[jpPrefixToCode[prefix]].push(id);
        } else {
            normalIds.push(id);
        }
    }

    const stats = {
        skippedExisting: 0,
        skippedNoData: 0,
        downloaded: 0,
        failed: 0,
    };

    const statsData = {
        skippedExisting: [],
        skippedNoData: [],
        downloaded: [],
        failed: [],
    };

    const tasks = normalIds.map(cardId => async () => {
        const card = getCard(cardId);

        if (!card) {
            stats.skippedNoData++;
            statsData.skippedNoData.push(cardId);
            return;
        }

        const spiritCode = spiritSetCodeFromCatalogId(cardId);

        if (!spiritCode) {
            stats.skippedNoData++;
            statsData.skippedNoData.push(cardId);
            return;
        }

        const dest = artPath(card, spiritCode);

        if (existsSync(dest)) {
            stats.skippedExisting++;
            statsData.skippedExisting.push(cardId);
            return;
        }

        try {
            await downloadFile(card.images.large, dest);
            stats.downloaded++;
            statsData.downloaded.push(cardId);

            console.log(`downloaded ${cardId} -> ${spiritCode}/${dest.split('/').pop()}`);
        } catch (err) {
            stats.failed++;
            statsData.failed.push(cardId);

            console.error(`failed ${cardId}: ${err.message}`);
        }
    });

    await runPool(tasks, CONCURRENCY);

    console.log('\nProcessing Free_Energy cards…');
    await handleFreeEnergy(stats, freeEnergyIds);

    for (const [spiritCode, limitlessId] of Object.entries(JP_SET_MAP)) {
        console.log(`\nProcessing ${spiritCode} (Limitless ${limitlessId})…`);

        await handleJpSet(
            spiritCode,
            limitlessId,
            stats,
            jpIdsByCode[spiritCode]
        );
    }

    console.log('\nDone.');
    console.log(`- downloaded:       ${stats.downloaded}`);
    console.log(`- already existed:  ${stats.skippedExisting}`);
    console.log(`- no data/mapping:  ${stats.skippedNoData}`);

    if (stats.failed) {
        console.log(`failed: ${stats.failed}`);
    }

    writeFileSync(
        join(rootDir, 'downloadedArtsStats.json'),
        JSON.stringify({ ...stats, ...statsData }, null, 2),
        'utf8'
    );
}

main();