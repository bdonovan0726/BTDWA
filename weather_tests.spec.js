const { test, expect } = require('@playwright/test');

const BASE_URL = process.env.BASE_URL || 'http://localhost';

test('BTDWA homepage loads', async ({ page }) => {
  await page.goto(BASE_URL);

  await expect(
    page.getByRole('heading', { name: 'BTDWA Weather' })
  ).toBeVisible();
});

test('Validate station cards displayed', async ({ page }) => {
    await page.goto(BASE_URL);

    const cards = page.locator('.station-card');
    const count = await cards.count();
    
    expect(count).toBeGreaterThan(0);
});

test('Validate headers display temps', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const headers = page.locator('.station-header');
    const count = await headers.count();
    for (let ctr = 0; ctr < count; ctr++){
        const text = await headers.nth(ctr).textContent();
        
        expect(text).toMatch(/\d+(\.\d+)?°C\s*\/\s*\d+(\.\d+)?°F/);

    }
    
});

test('Validate cards display forecast', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const cards = page.locator('.station-card');
    const count = await cards.count();
    for (let ctr = 0; ctr < count; ctr++){
        const curStation = cards.nth(ctr);
        await curStation.click();
        const lastPrecip = curStation.locator('.last-precip');
        await expect(lastPrecip).toHaveText(/^([1-9]|1[0-2])\/([0-9]|[1-2][0-9]|[3][0-1])\/(202[6-9]),\s([0-9]|1[0-2]):[0-5][0-9]:[0-5][0-9]\s(AM|PM)$/);
        const forecastTable = curStation.locator('.forecast-body');
        const rows = forecastTable.locator('tr');
        await expect(rows).toHaveCount(6);
        const rowCount = await rows.count();
        
        for (let x = 0; x < rowCount; x++){
            
            const curRow = rows.nth(x);
            const timeField = curRow.locator('td').nth(0);
            await expect(timeField).toHaveText(/^(0?[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM)$/);
            const tempField = curRow.locator('td').nth(1);
            await expect(tempField).toHaveText(/^-?\d+(?:\.\d+)?°C\s*\/\s*-?\d+(?:\.\d+)?°F$/);
            const precipField = curRow.locator('td').nth(2);
            await expect(precipField).toHaveText(/^\d+\.\d+\s*mm$/);
            
        }

    }
    
});