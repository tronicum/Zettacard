import { defineConfig } from '@playwright/test';
export default defineConfig({ testDir: '.', timeout: 20000, workers: 1, reporter: 'list' });
