import { type Page, expect, test } from "@playwright/test";
import { firstSuperuser, firstSuperuserPassword } from "./config.ts";
// import { randomPassword } from "./utils/random.ts";

test.use({ storageState: { cookies: [], origins: [] } });

const fillForm = async (page: Page, email: string, password: string) => {
  await page.getByPlaceholder("Email").fill(email);
  await page.getByPlaceholder("Password", { exact: true }).fill(password);
};

const searchTodo = async (page: Page, keyword: string) => {
  await page.getByPlaceholder("Search").fill(keyword);
  await page.getByRole("button", { name: "Search" }).click();
  await page.waitForTimeout(1000);
};

test("Log in and search for a Todo", async ({ page }) => {
  await page.goto("/login");

  await fillForm(page, firstSuperuser, firstSuperuserPassword);
  await page.getByRole("button", { name: "Log In" }).click();
  await page.waitForURL("/");

  await page.getByRole("link", { name: "Todo" }).click();
  await page.waitForURL("/todos");

  const keyword = "đồ án";
  await searchTodo(page, keyword);

  const todoItems = await page.locator("table tbody tr").all();

  expect(todoItems.length).toBeGreaterThan(0);

  for (const item of todoItems) {
    const title = await item.locator("td:nth-child(2)").textContent();
    const description = await item.locator("td:nth-child(3)").textContent();

    console.log(`🔍 Expected keyword: ${keyword}`);
    console.log(`📜 Received title: ${title?.toLowerCase()}`);
    console.log(`📜 Received description: ${description?.toLowerCase()}`);
    expect(title?.toLowerCase().includes(keyword) || description?.toLowerCase().includes(keyword)).toBeTruthy();
  }

  console.log("✅ Search is working correctly");
});
