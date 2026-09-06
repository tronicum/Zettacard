/**
 * DN-96 / ADR-0001. Serves app/ (the Netlify publish root) and runs the
 * multilingual exam suite against it.
 *
 * Chromium only by default: the questions this suite answers are exam-logic
 * and data questions, not rendering ones. WebKit matters for the mobile
 * layout work instead - see docs/adr/ADR-mobile-layout.md.
 */
import { defineConfig, devices } from '@playwright/test';

const PORT = process.env.PORT || 8802;

export default defineConfig({
  testDir: './tests/e2e',
  // A full exam run is ~30 questions of clicking; give it room.
  timeout: 120_000,
  expect: { timeout: 10_000 },
  fullyParallel: true,
  workers: process.env.CI ? 2 : 4,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['list'], ['json', { outputFile: 'tmp/e2e-report.json' }]] : 'list',
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: 'retain-on-failure',
    // detectLang() reads navigator.languages on first visit, before the
    // module picker renders and while #lang-select is still inert - so the
    // context locale, not the dropdown, is how a test selects its language.
    // Overridden per-project below.
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: `node scripts/serve-app.mjs ${PORT}`,
    url: `http://localhost:${PORT}/app.html`,
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});
