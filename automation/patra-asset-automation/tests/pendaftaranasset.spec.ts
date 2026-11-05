import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://demo-easset.patra-jasa.com/web/login');
});