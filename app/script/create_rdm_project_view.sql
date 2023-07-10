CREATE OR REPLACE ALGORITHM = UNDEFINED DEFINER = `test`@`%` SQL SECURITY DEFINER VIEW `zentao`.`rdm_project` AS SELECT
	`p`.`id` AS `id`,
	`p`.`type` AS `type`,
	`p`.`name` AS `name`,
	`p`.`code` AS `code`,
	`p`.`begin` AS `begin`,
	`p`.`end` AS `end`,
	`p`.`days` AS `days`,
	`p`.`status` AS `status`,
	`p`.`openedDate` AS `createDate`,
	`p`.`PM` AS `Leader`,
	`pp`.`product` AS `product`,
	`p`.`openedBy` AS `createUser`
FROM
	(
		`zt_project` `p`
	LEFT JOIN `zt_projectproduct` `pp` ON ( `p`.`id` = `pp`.`project` ))
WHERE
	`p`.`deleted` = '0'
	AND `p`.`status` IN (
	'wait',
	'doing');