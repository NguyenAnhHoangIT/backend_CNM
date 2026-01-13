USE shop;

-- 1. Dữ liệu Roles
INSERT INTO `Roles` (`Id`, `Name`, `NormalizedName`, `ConcurrencyStamp`) VALUES 
('869e2ef9-ecf2-4bf6-b2d7-e32f9dc65f13', 'Customer', 'CUSTOMER', NULL),
('adbf8b22-fe2a-495b-a182-f67d894d1ee4', 'Admin', 'ADMIN', NULL);

-- 2. Dữ liệu Users (Thêm cột Status)
INSERT INTO `Users` (`Id`, `FullName`, `AvatarUrl`, `UserName`, `NormalizedUserName`, `Email`, `NormalizedEmail`, `EmailConfirmed`, `PasswordHash`, `SecurityStamp`, `ConcurrencyStamp`, `PhoneNumber`, `PhoneNumberConfirmed`, `TwoFactorEnabled`, `LockoutEnd`, `LockoutEnabled`, `AccessFailedCount`, `Status`) VALUES 
('3137c58d-96f9-4284-8344-69bbc3d693a7', 'Admin', NULL, 'Admin@gmail.com', 'ADMIN@GMAIL.COM', 'Admin@gmail.com', 'ADMIN@GMAIL.COM', 1, 'AQAAAAIAAYagAAAAEJKWLphTpDoy+xsu4YDVg0GyoM/w4WFo3gr/qI1NRDcLbZi1eXoPeSF6MYANM9Rokg==', 'B27MI72C6X7QCKM463WD4SC6BTAQ365O', '917e8ce2-d002-4e80-87f9-9b0f5bc5dc6e', '0898866467', 0, 0, NULL, 1, 0, 1),
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Nguyễn Nhật Khánh', '/Uploads/638846725149581016_Doraemon_character.png', 'test@gmail.com', 'TEST@GMAIL.COM', 'test@gmail.com', 'TEST@GMAIL.COM', 0, 'AQAAAAIAAYagAAAAEDSRlcMVvXwzcIyHvTh7+6TOSNptY2WVF6nc6N2oJLjg372oymuvMgBbEu4gfIvqeA==', 'ARXXQYRFIXY3RHP3T4XAMJ4TZT3TZ725', '127d689c-18f3-4dcb-a4e3-0fe2eecac589', '0898866467', 0, 0, NULL, 1, 0, 1),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e', 'Nguyễn Khách', NULL, 'test01@gmail.com', 'TEST01@GMAIL.COM', 'test01@gmail.com', 'TEST01@GMAIL.COM', 0, 'AQAAAAIAAYagAAAAEPtFVsCfeRUeELchNYJmAgYekhB8eWbJDaeHY2W1oiDsYWDAuL4hf0gq4Zz+1RClsw==', '7S4KGNZ6BVTJXF34S5BZZIEEAINILP5I', '187c8065-04bc-4f8b-987f-32bcbf05a965', '0898866467', 0, 0, NULL, 1, 0, 1);

-- 3. Dữ liệu UserRoles
INSERT INTO `UserRoles` (`UserId`, `RoleId`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', '869e2ef9-ecf2-4bf6-b2d7-e32f9dc65f13'),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e', '869e2ef9-ecf2-4bf6-b2d7-e32f9dc65f13'),
('3137c58d-96f9-4284-8344-69bbc3d693a7', 'adbf8b22-fe2a-495b-a182-f67d894d1ee4');

-- 4. Dữ liệu Vouchers (Bảng mới theo ERD)
INSERT INTO `Vouchers` (`Id`, `Name`, `Description`, `Quantity`, `Discount`, `Status`, `CreateAt`, `UserId`) VALUES 
(1, 'WELCOME2025', 'Giảm giá chào mừng 50k', 100, 50000.00, 1, '2025-01-01 00:00:00', '3137c58d-96f9-4284-8344-69bbc3d693a7');

-- 5. Dữ liệu Categories (Thêm CreateAt, Status)
INSERT INTO `Categories` (`Id`, `Name`, `Description`, `ImageUrl`, `CreateAt`, `Status`) VALUES 
(1, 'Dụng cụ lưu trữ', 'Dụng cụ lưu trữ', '/assets/images/Categories03.jpg', '2025-01-01 00:00:00', 1),
(2, 'Bàn ghế và sofa', 'Bàn ghế và sofa', '/assets/images/Categories05.jpg', '2025-01-01 00:00:00', 1),
(3, 'Giường ngủ', 'Giường ngủ', '/assets/images/Categories07.jpg', '2025-01-01 00:00:00', 1),
(4, 'Kệ lưu trữ', 'Kệ lưu trữ', '/assets/images/Categories01.jpg', '2025-01-01 00:00:00', 1),
(5, 'Phụ kiện trang trí', 'Phụ kiện trang trí', '/assets/images/Categories02.jpg', '2025-01-01 00:00:00', 1),
(6, 'Phòng khách tiện nghi', 'Phòng khách tiện nghi', '/assets/images/Categories06.jpg', '2025-01-01 00:00:00', 1),
(7, 'Tinh dầu, nến và dầu thơm', 'Tinh dầu, nến và dầu thơm', '/assets/images/Categories04.jpg', '2025-01-01 00:00:00', 1);

-- 6. Dữ liệu Products (Thêm Status)
INSERT INTO `Products` (`Id`, `Name`, `Description`, `CreateAt`, `Status`, `CategoryId`) VALUES 
(1, 'Quạt Điện Đứng Có Remote', 'Quạt Điện Đứng Có Remote - Công Suất 24V-20W', '2025-05-24 00:00:00', 1, 6),
(3, 'Sofa Thư Giãn 1 Chỗ Ngồi', 'Sofa Thư Giãn 1 Chỗ Ngồi (Không Kèm Vỏ Nệm)', '2025-05-24 00:00:00', 1, 2);

-- 8. Dữ liệu ProductTypes (Fixed column name to ProductId)
INSERT INTO `ProductTypes` (`Id`, `Name`, `Quantity`, `Status`, `ProductId`, `ImageUrl`) VALUES 
(1, 'Màu đen', 200, 1, 1, '/assets/images/product01.jpg'),
(3, 'Màu trắng', 200, 1, 1, '/assets/images/product02.jpg'),
(4, 'Màu trắng', 200, 1, 3, '/assets/images/product03.jpg'); -- Linked to Sofa (Product 3)

-- 9. Dữ liệu PriceItem (Đổi tên từ PriceItems)
INSERT INTO `PriceItem` (`Id`, `Number`, `Price`, `ProductTypeId`) VALUES 
(1, 100, 200000.00, 1),
(2, 200, 170000.00, 1),
(3, 300, 150000.00, 1),
(5, 100, 200000.00, 3),
(6, 200, 170000.00, 3),
(7, 300, 150000.00, 3),
(8, 50, 5000000.00, 4),
(9, 100, 4600000.00, 4),
(11, 150, 4200000.00, 4);

-- 10. Dữ liệu Invoices (Đổi ToTal thành Total, bỏ Deposit/PaymentCode, thêm VoucherId)
INSERT INTO `Invoices` (`Id`, `UserId`, `Address`, `Total`, `Status`, `CreateAt`, `VoucherId`) VALUES 
(1, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', '136 Trần Cao Vân', 1000000.00, 0, '2025-05-24 00:00:00', 1),
(2, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Chưa cập nhật', 400000.00, -1, '2025-06-06 11:16:40', NULL),
(3, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Chưa cập nhật', 4000000.00, -1, '2025-06-06 13:15:07', NULL);

-- 11. Dữ liệu InvoicesItem
INSERT INTO `InvoicesItem` (`InvoiceId`, `ProductTypeId`, `Quantity`, `Amount`) VALUES 
(1, 1, 15, 200000.00),
(1, 3, 30, 200000.00),
(2, 1, 2, 400000.00),
(3, 3, 17, 3400000.00);

-- 12. Dữ liệu Ratings (Bảng mới)
INSERT INTO `Ratings` (`Id`, `Stars`, `Comment`, `InvoiceId`, `CreateAt`) VALUES 
(1, 5, 'Sản phẩm tuyệt vời, đóng gói kỹ', 1, '2025-05-25 10:00:00');

-- 13. Dữ liệu Favorites & FavouriteProducts
INSERT INTO `Favorites` (`UserId`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd'),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e');

INSERT INTO `FavoriteProducts` (`FavoriteId`, `ProductId`, `CreateAt`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 1, '2025-01-01 00:00:00'),
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 3, '2025-01-01 00:00:00');

-- 14. Dữ liệu ProductImages
INSERT INTO `ProductImages` (`Id`, `Url`, `Description`, `ProductId`) VALUES 
(1, '/assets/images/product01.jpg', 'Ảnh sản phẩm 1', 1),
(2, '/assets/images/product17.jpg', 'Ảnh sản phẩm 2', 3);

-- 15. Dữ liệu Notifications (Bảng mới)
INSERT INTO `Notifications` (`Id`, `Title`, `Content`, `CreateAt`, `Status`, `ReceiverId`) VALUES 
(1, 'Đơn hàng mới', 'Bạn có một đơn hàng đang chờ xác nhận', '2025-06-06 13:00:00', 0, '3137c58d-96f9-4284-8344-69bbc3d693a7');

-- 16. Dữ liệu Cart
INSERT INTO `Cart` (`UserId`, `CreateAt`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', '2026-01-08 10:00:00'),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e', '2026-01-08 10:05:00');

-- 17. Dữ liệu CartItem
-- Nguyễn Nhật Khánh (74dcf6d8...) thêm 2 Quạt Màu đen (ProductType 1) vào giỏ
-- Nguyễn Khách (9a9363e3...) thêm 1 Quạt Màu trắng (ProductType 3) vào giỏ
INSERT INTO `CartItem` (`CartId`, `ProductTypeId`, `Quantity`, `CreateAt`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 1, 2, '2026-01-08 10:10:00'),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e', 3, 1, '2026-01-08 10:15:00');