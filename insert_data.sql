USE shop;

-- Dữ liệu AspNetRoles
INSERT INTO `Roles` (`Id`, `Name`, `NormalizedName`, `ConcurrencyStamp`) VALUES 
('869e2ef9-ecf2-4bf6-b2d7-e32f9dc65f13', 'Customer', 'CUSTOMER', NULL),
('adbf8b22-fe2a-495b-a182-f67d894d1ee4', 'Admin', 'ADMIN', NULL);

-- Dữ liệu AspNetUsers
INSERT INTO `Users` (`Id`, `FullName`, `AvatarUrl`, `UserName`, `NormalizedUserName`, `Email`, `NormalizedEmail`, `EmailConfirmed`, `PasswordHash`, `SecurityStamp`, `ConcurrencyStamp`, `PhoneNumber`, `PhoneNumberConfirmed`, `TwoFactorEnabled`, `LockoutEnd`, `LockoutEnabled`, `AccessFailedCount`) VALUES 
('3137c58d-96f9-4284-8344-69bbc3d693a7', 'Admin', NULL, 'Admin@gmail.com', 'ADMIN@GMAIL.COM', 'Admin@gmail.com', 'ADMIN@GMAIL.COM', 1, 'AQAAAAIAAYagAAAAEJKWLphTpDoy+xsu4YDVg0GyoM/w4WFo3gr/qI1NRDcLbZi1eXoPeSF6MYANM9Rokg==', 'B27MI72C6X7QCKM463WD4SC6BTAQ365O', '917e8ce2-d002-4e80-87f9-9b0f5bc5dc6e', '0898866467', 0, 0, NULL, 1, 0),
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Nguyễn Nhật Khánh', '/Uploads/638846725149581016_Doraemon_character.png', 'test@gmail.com', 'TEST@GMAIL.COM', 'test@gmail.com', 'TEST@GMAIL.COM', 0, 'AQAAAAIAAYagAAAAEDSRlcMVvXwzcIyHvTh7+6TOSNptY2WVF6nc6N2oJLjg372oymuvMgBbEu4gfIvqeA==', 'ARXXQYRFIXY3RHP3T4XAMJ4TZT3TZ725', '127d689c-18f3-4dcb-a4e3-0fe2eecac589', '0898866467', 0, 0, NULL, 1, 0),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e', 'Nguyễn Khách', NULL, 'test01@gmail.com', 'TEST01@GMAIL.COM', 'test01@gmail.com', 'TEST01@GMAIL.COM', 0, 'AQAAAAIAAYagAAAAEPtFVsCfeRUeELchNYJmAgYekhB8eWbJDaeHY2W1oiDsYWDAuL4hf0gq4Zz+1RClsw==', '7S4KGNZ6BVTJXF34S5BZZIEEAINILP5I', '187c8065-04bc-4f8b-987f-32bcbf05a965', '0898866467', 0, 0, NULL, 1, 0);

-- Dữ liệu AspNetUserRoles
INSERT INTO `UserRoles` (`UserId`, `RoleId`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', '869e2ef9-ecf2-4bf6-b2d7-e32f9dc65f13'),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e', '869e2ef9-ecf2-4bf6-b2d7-e32f9dc65f13'),
('3137c58d-96f9-4284-8344-69bbc3d693a7', 'adbf8b22-fe2a-495b-a182-f67d894d1ee4');

-- Dữ liệu Categories
INSERT INTO `Categories` (`Id`, `Name`, `Description`, `ImageUrl`) VALUES 
(1, 'Dụng cụ lưu trữ', 'Dụng cụ lưu trữ', '/assets/images/Categories03.jpg'),
(2, 'Bàn ghế và sofa', 'Bàn ghế và sofa', '/assets/images/Categories05.jpg'),
(3, 'Giường ngủ', 'Giường ngủ', '/assets/images/Categories07.jpg'),
(4, 'Kệ lưu trữ', 'Kệ lưu trữ', '/assets/images/Categories01.jpg'),
(5, 'Phụ kiện trang trí', 'Phụ kiện trang trí', '/assets/images/Categories02.jpg'),
(6, 'Phòng khách tiện nghi', 'Phòng khách tiện nghi', '/assets/images/Categories06.jpg'),
(7, 'Tinh dầu, nến và dầu thơm', 'Tinh dầu, nến và dầu thơm', '/assets/images/Categories04.jpg');

-- Dữ liệu Favorites
INSERT INTO `Favorites` (`UserId`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd'),
('9a9363e3-0a77-48c9-9e1b-db125b0ea80e');

-- Dữ liệu Products
INSERT INTO `Products` (`Id`, `Name`, `Description`, `CreateAt`, `CategoryId`) VALUES 
(1, 'Quạt Điện Đứng Có Remote - Công Suất 24V-20W', 'Quạt Điện Đứng Có Remote - Công Suất 24V-20W', '2025-05-24 00:00:00', 6),
(3, 'Sofa Thư Giãn 1 Chỗ Ngồi (Không Kèm Vỏ Nệm)', 'Sofa Thư Giãn 1 Chỗ Ngồi (Không Kèm Vỏ Nệm)', '2025-05-24 00:00:00', 2);

-- Dữ liệu FavouriteProducts
INSERT INTO `FavouriteProducts` (`FavouriteId`, `ProductId`, `CreateAt`) VALUES 
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 1, '2025-01-01 00:00:00'),
('74dcf6d8-31f5-45d8-8429-130cc188c4dd', 3, '2025-01-01 00:00:00');

-- Dữ liệu Invoices
INSERT INTO `Invoices` (`Id`, `UserId`, `Address`, `Status`, `CreateAt`, `Deposit`, `ToTal`, `PaymentCode`) VALUES 
(1, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', '136 Trần Cao Vân', 0, '2025-05-24 00:00:00', 0.00, 0.00, ''),
(2, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Chưa cập nhật', -100, '2025-06-06 11:16:40', 300000.00, 0.00, 'temp'),
(3, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Chưa cập nhật', -100, '2025-06-06 13:15:07', 1200000.00, 0.00, '74dcf6d8-31f5-45d8-8429-130cc188c4dd6/6/2025 1:15:13 PM'),
(4, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Chưa cập nhật', -1, '2025-06-06 13:27:28', 6000000.00, 0.00, '74dcf6d8-31f5-45d8-8429-130cc188c4dd6/6/2025 1:27:33 PM'),
(5, '74dcf6d8-31f5-45d8-8429-130cc188c4dd', 'Chưa cập nhật', 0, '2025-06-06 13:57:41', 6000000.00, 0.00, '74dcf6d8-31f5-45d8-8429-130cc188c4dd6/6/2025 1:57:48 PM');

-- Dữ liệu ProductLaunchs
INSERT INTO `ProductLaunchs` (`Id`, `Name`, `Description`, `DateStart`, `DateEnd`, `ProductId`) VALUES 
(1, 'Mở bán lần đầu', 'Mở bán lần đầu', '2025-05-24 00:00:00', '2025-06-09 00:00:00', 1),
(4, 'Mở bán lần đầu', 'Mở bán lần đầu', '2025-05-24 00:00:00', '2025-05-28 00:00:00', 3);

-- Dữ liệu ProductTypes
INSERT INTO `ProductTypes` (`Id`, `Name`, `Quantity`, `ProductLaunchId`, `ImageUrl`, `MaxPrice`, `MinPrice`) VALUES 
(1, 'Màu đen', 200, 1, '/assets/images/product01.jpg', 230000.00, 0.00),
(3, 'Màu trắng', 200, 1, '/assets/images/product02.jpg', 230000.00, 0.00),
(4, 'Màu trắng', 200, 4, '/assets/images/product03.jpg', 5400000.00, 0.00);

-- Dữ liệu InvoicesItem
INSERT INTO `InvoicesItem` (`InvoiceId`, `ProductTypeId`, `Quantity`, `Amount`) VALUES 
(1, 1, 15, 0.00),
(1, 3, 30, 0.00),
(2, 1, 2, 400000.00),
(2, 3, 3, 600000.00),
(3, 1, 3, 600000.00),
(3, 3, 17, 3400000.00),
(4, 1, 100, 20000000.00),
(5, 1, 50, 10000000.00),
(5, 3, 50, 10000000.00);

-- Dữ liệu PriceItems
INSERT INTO `PriceItems` (`Id`, `Number`, `Price`, `ProductTypeId`) VALUES 
(1, 100, 200000.00, 1),
(2, 200, 170000.00, 1),
(3, 300, 150000.00, 1),
(5, 100, 200000.00, 3),
(6, 200, 170000.00, 3),
(7, 300, 150000.00, 3),
(8, 50, 5000000.00, 4),
(9, 100, 4600000.00, 4),
(11, 150, 4200000.00, 4);

-- Dữ liệu ProductImages
INSERT INTO `ProductImages` (`Id`, `Url`, `Description`, `ProductId`) VALUES 
(1, '/assets/images/product01.jpg', 'Ảnh sản phẩm', 1),
(2, '/assets/images/product17.jpg', 'Ảnh sản phẩm', 3),
(5, '/assets/images/product02.jpg', 'Ảnh sản phẩm', 1),
(7, '/assets/images/product03.jpg', 'Ảnh sản phẩm', 1),
(8, '/assets/images/product04.jpg', 'Ảnh sản phẩm', 3),
(9, '/assets/images/product05.jpg', 'Ảnh sản phẩm', 3);