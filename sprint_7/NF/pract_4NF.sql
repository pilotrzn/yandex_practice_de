/*Создание таблицы nf_lesson.subject_teacher_4nf*/

DROP TABLE IF EXISTS nf_lesson.subject_teacher_4nf;
CREATE TABLE nf_lesson.subject_teacher_4nf AS
SELECT DISTINCT subject,teacher
FROM nf_lesson.source_4nf; 

/*Создание таблицы nf_lesson.subject_book_4nf*/

DROP TABLE IF EXISTS nf_lesson.subject_book_4nf;
CREATE TABLE nf_lesson.subject_book_4nf AS
SELECT DISTINCT subject,book 
FROM nf_lesson.source_4nf; 