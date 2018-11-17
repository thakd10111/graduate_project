-- 1. 근육근육 팔 - muscular_arm
-- 2. 태평양 어깨 - broad_shoulders
-- 3. 내장지방 안녕 - bye_internal_fat
-- 4. 초콜릿 복근 - chocolate_abs
-- 5. 단기 체중 감량 - short_term_weight_loss
-- 6. 칼로리 소모 플랜 - caloric_consumption_plans
-- 7. 튼튼 허벅지 - strong_thighs
-- 8. 코어 근육 강화 - strengthen_core_muscles
-- 9. 임산부 운동 - pregnant_womens_exer

insert into ROUTINETHEME (theme_num, theme, step1, step2, step3, step4) values
	(1, 'muscular_arm', 1, 2, 3, 4),
	(2, 'broad_shoulders', 1, 2, 3, 4),
	(3, 'bye_internal_fat', 1, 2, 3, 4),
	(4, 'chocolate_abs', 1, 2, 3, 4),
	(5, 'short_term_weight_loss', 1, 2, 3, 4),
	(6, 'caloric_consumption_plans', 1, 2, 3, 4),
	(7, 'strong_thighs', 1, 2, 3, 4),
	(8, 'strengthen_core_muscles', 1, 2, 3, 4),
	(9, 'pregnant_womens_exer', 1, 2, 3, 4);


insert into DETAILSTEP (theme_num, step_num, length, timing, bodypart, excer_type, equipment) values
	(1, 1, 3, 'daily', 'arm', 'stretching', 'dc'),
	(1, 2, 15, 'daily', 'front_arm', 'circuit,weight', 'babell,dumbbell'),
	(1, 3, 10, 'daily', 'back_arm', 'circuit,weight', 'babell,dumbbell'),
	(1, 4, 10, 'daily', 'arm', 'stretching', 'dc'),
	(2, 1, 10, 'daily', 'shoulder', 'weight', 'babell,dumbbell'),
	(2, 2, 20, 'daily', 'side_neck', 'weight', 'dumbbell'),
	(2, 3, 10, 'daily', 'shoulder', 'weight', 'shoulder_press,butterfly'),
	(2, 4, 10, 'daily', 'shoulder', 'stretching', 'dc'),
	(3, 1, 10, 'daily', 'whole', 'interval', 'treadmill'),
	(3, 2, 5, 'daily', 'whole', 'stretching', 'dc'),
	(3, 3, 40, 'daily', 'whole', 'circuit,weight', 'dc'),
	(3, 4, 30, 'daily', 'whole', 'interval', 'treadmill'),
	(4, 1, 15, 'daily', 'belly', 'weight', 'dc'),
	(4, 2, 10, 'daily', 'waist', 'circuit,weight', 'dc'),
	(4, 3, 10, 'daily', 'belly', 'circuit', 'dc'),
	(4, 4, 10, 'daily', 'belly', 'stretching', 'dc'),
	(5, 1, 10, 'daily,overeating', 'whole', 'interval', 'dc'),
	(5, 2, 40, 'daily,overeating', 'whole', 'circuit,weight', 'dc'),
	(5, 3, 30, 'daily,overeating', 'whole', 'interval', 'dc'),
	(5, 4, 10, 'daily,overeating', 'whole', 'stretching', 'dc'),
	(6, 1, 5, 'overeating', 'whole', 'circuit,weight', 'dc'),
	(6, 2, 5, 'overeating', 'thigh', 'circuit,weight', 'dc'),
	(6, 3, 5, 'overeating', 'belly', 'circuit,weight', 'dc'),
	(6, 4, 10, 'overeating', 'whole', 'stretching', 'dc'),
	(7, 1, 5, 'daily', 'leg', 'circuit,weight', 'dc'),
	(7, 2, 5, 'daily', 'thigh', 'circuit,weight', 'dc'),
	(7, 3, 5, 'daily', 'hip', 'circuit,weight', 'dc'),
	(7, 4, 10, 'daily', 'leg', 'stretching', 'dc'),
	(8, 1, 5, 'daily', 'belly', 'circuit,weight', 'dc'),
	(8, 2, 5, 'daily', 'waist', 'circuit,weight', 'dc'),
	(8, 3, 5, 'daily', 'side', 'circuit,weight', 'dc'),
	(8, 4, 10, 'daily', 'belly', 'stretching', 'dc'),
	(9, 1, 30, 'daily', 'whole', 'stretching', 'dc'),
	(9, 2, 30, 'daily', 'whole', 'weight', 'dc'),
	(9, 3, 30, 'daily', 'whole', 'interval', 'dc'),
	(9, 4, 10, 'daily', 'whole', 'stretching', 'dc');
