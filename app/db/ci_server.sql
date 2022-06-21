/*
 Navicat Premium Data Transfer

 Source Server         : 禅道
 Source Server Type    : MySQL
 Source Server Version : 100414
 Source Host           : 192.168.1.43:3306
 Source Schema         : zentao

 Target Server Type    : MySQL
 Target Server Version : 100414
 File Encoding         : 65001

 Date: 18/05/2022 18:53:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ci_server
-- ----------------------------
DROP TABLE IF EXISTS `ci_server`;
CREATE TABLE `ci_server`  (
  `id` mediumint NOT NULL AUTO_INCREMENT,
  `ipAddress` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'IP地址',
  `serverName` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '服务器名称',
  `remark` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `deleted` enum('0','1') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0' COMMENT '删除标记，1标识已删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
