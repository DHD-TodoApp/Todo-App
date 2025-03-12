import { type Page, expect, test } from "@playwright/test";
import { firstSuperuser, firstSuperuserPassword } from "./config.ts";

test.use({ storageState: { cookies: [], origins: [] } });

const login = async (page: Page) => {
  await page.goto("/login");

  await page.getByPlaceholder("Email").fill(firstSuperuser);
  await page.getByPlaceholder("Password", { exact: true }).fill(firstSuperuserPassword);

  await page.getByRole("button", { name: "Log In" }).click();
  await page.waitForURL("/");
};

const addTodo = async (page: Page, title: string, description: string) => {
  await page.getByRole("link", { name: "Todo" }).click();
  await page.waitForURL("/todos");

  await page.getByRole("button", { name: "Add Todo" }).click();

  await page.getByPlaceholder("Title").fill(title);
  await page.getByPlaceholder("Description").fill(description);
  await page.getByRole("button", { name: "Save" }).click();

  await page.waitForTimeout(1000);
};

const searchTodo = async (page: Page, keyword: string) => {
  await page.getByPlaceholder("Search").fill(keyword);
  await page.getByRole("button", { name: "Search" }).click();
  await page.waitForTimeout(1000);
};

test("Người dùng có thể thêm một Todo mới", async ({ page }) => {
  await login(page);

  const newTitle = "Viết báo cáo";
  const newDescription = "Viết báo cáo môn Khoa học máy tính";

  await addTodo(page, newTitle, newDescription);
  await searchTodo(page, newTitle);

  const todoItems = await page.locator("table tbody tr").all();
  expect(todoItems.length).toBeGreaterThan(0);

  for (const item of todoItems) {
    const title = await item.locator("td:nth-child(2)").textContent();
    const description = await item.locator("td:nth-child(3)").textContent();

    console.log(`📜 Expected title: ${newTitle}`);
    console.log(`📜 Expected description: ${newDescription}`);
    console.log(`🔍 Received title: ${title}`);
    console.log(`🔍 Received description: ${description}`);

    expect(title?.trim()).toBe(newTitle);
    expect(description?.trim()).toBe(newDescription);
  }

  console.log("✅ Todo has been added successfully!");
});
