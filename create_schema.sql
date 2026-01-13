CREATE DATABASE IF NOT EXISTS shop;
USE shop;

-- 1. Identity Tables (Giữ nguyên cấu trúc cơ bản, thêm Status cho Users)
CREATE TABLE `Roles` (
  `Id` varchar(255) NOT NULL,
  `Name` varchar(256) DEFAULT NULL,
  `NormalizedName` varchar(256) DEFAULT NULL,
  `ConcurrencyStamp` longtext DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB;

CREATE TABLE `Users` (
  `Id` varchar(255) NOT NULL,
  `FullName` longtext NOT NULL,
  `AvatarUrl` longtext DEFAULT NULL,
  `UserName` varchar(256) DEFAULT NULL,
  `NormalizedUserName` varchar(256) DEFAULT NULL,
  `Email` varchar(256) DEFAULT NULL,
  `NormalizedEmail` varchar(256) DEFAULT NULL,
  `EmailConfirmed` boolean NOT NULL,
  `PasswordHash` longtext DEFAULT NULL,
  `SecurityStamp` longtext DEFAULT NULL,
  `ConcurrencyStamp` longtext DEFAULT NULL,
  `PhoneNumber` longtext DEFAULT NULL,
  `PhoneNumberConfirmed` boolean NOT NULL,
  `TwoFactorEnabled` boolean NOT NULL,
  `LockoutEnd` datetime(6) DEFAULT NULL,
  `LockoutEnabled` boolean NOT NULL,
  `AccessFailedCount` int NOT NULL,
  `Status` int NOT NULL DEFAULT 1, -- Thêm từ ERD
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB;

-- 2. Notifications (Bảng mới)
CREATE TABLE `Notifications` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Title` longtext NOT NULL,
  `Content` longtext NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `ReadAt` datetime(6) DEFAULT NULL,
  `Status` int NOT NULL,
  `ReceiverId` varchar(255) NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Notifications_Users_ReceiverId` FOREIGN KEY (`ReceiverId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Vouchers (Bảng mới - Cần tạo trước Invoices)
CREATE TABLE `Vouchers` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Description` longtext,
  `Quantity` int NOT NULL,
  `Discount` decimal(18,2) NOT NULL,
  `Status` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `UserId` varchar(255) NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Vouchers_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Categories (Thêm CreateAt, Status)
CREATE TABLE `Categories` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `ImageUrl` longtext NOT NULL,
  `CreateAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `Status` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB;

-- 5. Products (Thêm Status)
CREATE TABLE `Products` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `Status` int NOT NULL DEFAULT 1,
  `CategoryId` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Products_Categories_CategoryId` FOREIGN KEY (`CategoryId`) REFERENCES `Categories` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. ProductTypes (Thêm Status)
CREATE TABLE `ProductTypes` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Quantity` int NOT NULL,
  `Status` int NOT NULL DEFAULT 1,
  `ProductId` int NOT NULL,
  `ImageUrl` longtext DEFAULT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_ProductTypes_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. PriceItem (Đổi tên từ PriceItems)
CREATE TABLE `PriceItem` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Number` int NOT NULL,
  `Price` decimal(18,2) NOT NULL,
  `ProductTypeId` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_PriceItem_ProductTypes_ProductTypeId` FOREIGN KEY (`ProductTypeId`) REFERENCES `ProductTypes` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. Invoices (Thêm VoucherId)
CREATE TABLE `Invoices` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `UserId` varchar(255) NOT NULL,
  `Address` longtext NOT NULL,
  `Total` decimal(18,2) NOT NULL DEFAULT 0.0,
  `Status` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `VoucherId` int DEFAULT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Invoices_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `FK_Invoices_Vouchers_VoucherId` FOREIGN KEY (`VoucherId`) REFERENCES `Vouchers` (`Id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 10. InvoicesItem
CREATE TABLE `InvoicesItem` (
  `InvoiceId` int NOT NULL,
  `ProductTypeId` int NOT NULL,
  `Quantity` int NOT NULL,
  `Amount` decimal(18,2) NOT NULL,
  PRIMARY KEY (`InvoiceId`, `ProductTypeId`),
  CONSTRAINT `FK_InvoicesItem_Invoices_InvoiceId` FOREIGN KEY (`InvoiceId`) REFERENCES `Invoices` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `FK_InvoicesItem_ProductTypes_ProductTypeId` FOREIGN KEY (`ProductTypeId`) REFERENCES `ProductTypes` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 11. Ratings & RatingMedia (Bảng mới)
CREATE TABLE `Ratings` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Stars` int NOT NULL,
  `Comment` longtext,
  `InvoiceId` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `UpdateAt` datetime(6) DEFAULT NULL,
  `DeleteAt` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Ratings_Invoices_InvoiceId` FOREIGN KEY (`InvoiceId`) REFERENCES `Invoices` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `RatingMedia` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Url` longtext NOT NULL,
  `RatingId` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_RatingMedia_Ratings_RatingId` FOREIGN KEY (`RatingId`) REFERENCES `Ratings` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 12. Favorites & FavoriteProducts
CREATE TABLE `Favorites` (
  `UserId` varchar(255) NOT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `FK_Favorites_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `FavoriteProducts` (
  `FavoriteId` varchar(255) NOT NULL,
  `ProductId` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  PRIMARY KEY (`FavoriteId`, `ProductId`),
  CONSTRAINT `FK_FavoriteProducts_Favorites_FavoriteId` FOREIGN KEY (`FavoriteId`) REFERENCES `Favorites` (`UserId`) ON DELETE CASCADE,
  CONSTRAINT `FK_FavoriteProducts_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 13. ProductImages
CREATE TABLE `ProductImages` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Url` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `ProductId` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_ProductImages_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 14. Identity Supports (Dư thừa theo ERD nhưng cần thiết cho chức năng)
CREATE TABLE `UserRoles` (
  `UserId` varchar(255) NOT NULL,
  `RoleId` varchar(255) NOT NULL,
  PRIMARY KEY (`UserId`, `RoleId`),
  CONSTRAINT `FK_UserRoles_Roles_RoleId` FOREIGN KEY (`RoleId`) REFERENCES `Roles` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `FK_UserRoles_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 15. Cart & CartItem
CREATE TABLE `Cart` (
  `UserId` varchar(255) NOT NULL,
  `CreateAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `UpdateAt` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `FK_Cart_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `CartItem` (
  `CartId` varchar(255) NOT NULL,
  `ProductTypeId` int NOT NULL,
  `Quantity` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`CartId`, `ProductTypeId`),
  CONSTRAINT `FK_CartItem_Cart_CartId` FOREIGN KEY (`CartId`) REFERENCES `Cart` (`UserId`) ON DELETE CASCADE,
  CONSTRAINT `FK_CartItem_ProductTypes_ProductTypeId` FOREIGN KEY (`ProductTypeId`) REFERENCES `ProductTypes` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;