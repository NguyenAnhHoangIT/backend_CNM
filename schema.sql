CREATE DATABASE IF NOT EXISTS shop;
USE shop;

-- 1. EFMigrationsHistory
CREATE TABLE `__EFMigrationsHistory` (
  `MigrationId` varchar(150) NOT NULL,
  `ProductVersion` varchar(32) NOT NULL,
  PRIMARY KEY (`MigrationId`)
) ENGINE=InnoDB;

-- 2. AspNetRoles
CREATE TABLE `Roles` (
  `Id` varchar(255) NOT NULL,
  `Name` varchar(256) DEFAULT NULL,
  `NormalizedName` varchar(256) DEFAULT NULL,
  `ConcurrencyStamp` longtext DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB;

-- 3. AspNetUsers
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
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB;

-- 4. AspNetRoleClaims
CREATE TABLE `RoleClaims` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `RoleId` varchar(255) NOT NULL,
  `ClaimType` longtext DEFAULT NULL,
  `ClaimValue` longtext DEFAULT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_RoleClaims_Roles_RoleId` FOREIGN KEY (`RoleId`) REFERENCES `Roles` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. AspNetUserClaims
CREATE TABLE `UserClaims` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `UserId` varchar(255) NOT NULL,
  `ClaimType` longtext DEFAULT NULL,
  `ClaimValue` longtext DEFAULT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_UserClaims_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. AspNetUserLogins
CREATE TABLE `UserLogins` (
  `LoginProvider` varchar(255) NOT NULL,
  `ProviderKey` varchar(255) NOT NULL,
  `ProviderDisplayName` longtext DEFAULT NULL,
  `UserId` varchar(255) NOT NULL,
  PRIMARY KEY (`LoginProvider`, `ProviderKey`),
  CONSTRAINT `FK_UserLogins_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. AspNetUserRoles
CREATE TABLE `UserRoles` (
  `UserId` varchar(255) NOT NULL,
  `RoleId` varchar(255) NOT NULL,
  PRIMARY KEY (`UserId`, `RoleId`),
  CONSTRAINT `FK_UserRoles_Roles_RoleId` FOREIGN KEY (`RoleId`) REFERENCES `Roles` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `FK_UserRoles_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. AspNetUserTokens
CREATE TABLE `UserTokens` (
  `UserId` varchar(255) NOT NULL,
  `LoginProvider` varchar(255) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Value` longtext DEFAULT NULL,
  PRIMARY KEY (`UserId`, `LoginProvider`, `Name`),
  CONSTRAINT `FK_UserTokens_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. Categories
CREATE TABLE `Categories` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `ImageUrl` longtext NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB;

-- 10. Favorites
CREATE TABLE `Favorites` (
  `UserId` varchar(255) NOT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `FK_Favorites_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 11. Products
CREATE TABLE `Products` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `CategoryId` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Products_Categories_CategoryId` FOREIGN KEY (`CategoryId`) REFERENCES `Categories` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 12. FavouriteProducts
CREATE TABLE `FavouriteProducts` (
  `FavouriteId` varchar(255) NOT NULL,
  `ProductId` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL DEFAULT '0001-01-01 00:00:00',
  PRIMARY KEY (`FavouriteId`, `ProductId`),
  CONSTRAINT `FK_FavouriteProducts_Favorites_FavouriteId` FOREIGN KEY (`FavouriteId`) REFERENCES `Favorites` (`UserId`) ON DELETE CASCADE,
  CONSTRAINT `FK_FavouriteProducts_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 13. Invoices
CREATE TABLE `Invoices` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `UserId` varchar(255) NOT NULL,
  `Address` longtext NOT NULL,
  `Status` int NOT NULL,
  `CreateAt` datetime(6) NOT NULL,
  `Deposit` decimal(18,2) NOT NULL DEFAULT 0.0,
  `ToTal` decimal(18,2) NOT NULL DEFAULT 0.0,
  `PaymentCode` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_Invoices_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 14. ProductLaunchs
CREATE TABLE `ProductLaunchs` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `DateStart` datetime(6) NOT NULL,
  `DateEnd` datetime(6) NOT NULL,
  `ProductId` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_ProductLaunchs_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 15. ProductTypes
CREATE TABLE `ProductTypes` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext NOT NULL,
  `Quantity` int NOT NULL,
  `ProductLaunchId` int NOT NULL,
  `ImageUrl` longtext DEFAULT NULL,
  `MaxPrice` decimal(18,2) NOT NULL DEFAULT 0.0,
  `MinPrice` decimal(18,2) NOT NULL DEFAULT 0.0,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_ProductTypes_ProductLaunchs_ProductLaunchId` FOREIGN KEY (`ProductLaunchId`) REFERENCES `ProductLaunchs` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 16. InvoicesItem
CREATE TABLE `InvoicesItem` (
  `InvoiceId` int NOT NULL,
  `ProductTypeId` int NOT NULL,
  `Quantity` int NOT NULL,
  `Amount` decimal(18,2) NOT NULL,
  PRIMARY KEY (`InvoiceId`, `ProductTypeId`),
  CONSTRAINT `FK_InvoicesItem_Invoices_InvoiceId` FOREIGN KEY (`InvoiceId`) REFERENCES `Invoices` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `FK_InvoicesItem_ProductTypes_ProductTypeId` FOREIGN KEY (`ProductTypeId`) REFERENCES `ProductTypes` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 17. PriceItems
CREATE TABLE `PriceItems` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Number` int NOT NULL,
  `Price` decimal(18,2) NOT NULL,
  `ProductTypeId` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_PriceItems_ProductTypes_ProductTypeId` FOREIGN KEY (`ProductTypeId`) REFERENCES `ProductTypes` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 18. ProductImages
CREATE TABLE `ProductImages` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Url` longtext NOT NULL,
  `Description` longtext NOT NULL,
  `ProductId` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `FK_ProductImages_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB;