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

test("Người dùng có thể chuyển đổi trạng thái của Todo", async ({ page }) => {
  await login(page);

  await page.getByRole("link", { name: "Todo" }).click();
  await page.waitForURL("/todos");

  // Tìm hàng đầu tiên trong bảng Todo
  const firstTodoRow = page.locator("table tbody tr").first();
  const statusButton = firstTodoRow.locator("td:nth-child(4) button.chakra-button");

  // Kiểm tra trạng thái ban đầu
  let currentStatus = await statusButton.textContent();
  expect(["In Progress", "Pending", "Completed"]).toContain(currentStatus?.trim());

  // Chuyển sang trạng thái tiếp theo
  await statusButton.click();
  await page.waitForTimeout(500);
  let newStatus = await statusButton.textContent();
  expect(newStatus?.trim()).not.toBe(currentStatus?.trim());

  // Chuyển tiếp
  currentStatus = newStatus;
  await statusButton.click();
  await page.waitForTimeout(500);
  newStatus = await statusButton.textContent();
  expect(newStatus?.trim()).not.toBe(currentStatus?.trim());

  // Quay lại trạng thái ban đầu
  currentStatus = newStatus;
  await statusButton.click();
  await page.waitForTimeout(500);
  newStatus = await statusButton.textContent();
  expect(newStatus?.trim()).not.toBe(currentStatus?.trim());

  console.log("✅ Todo status has been successfully!");
});
