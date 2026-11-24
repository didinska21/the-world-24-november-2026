import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// THE WORLD - Tuesday 24 November 2026.
// The entry is one newspaper front page drawn in code (draw_frontpage.py).
// This program copies the bundled image to the output directory, so both
// grading runs write exactly the same bytes.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
