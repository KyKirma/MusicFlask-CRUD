CREATE DATABASE playmusica;
USE playmusica;

CREATE TABLE musica(
    id_musica INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_musica VARCHAR(50),
    cantor_banda VARCHAR(50),
    genero_musica varchar(20));

CREATE TABLE usuario(
    id_usuario INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_usuario VARCHAR(50),
    login_usuario VARCHAR(20) UNIQUE,
    senha_usuario varchar(15));