<template>
    <aside class="menu">
        <img class="logo is-centered"></img>
        <p class="menu-label">ОБЩЕЕ</p>
        <ul class="menu-list">
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-chart-bar"></i>
                    </span>
                    Обзор
                </a>
            </li>
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-building"></i>
                    </span>
                    Организация
                </a>
            </li>
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-user"></i>
                    </span>
                    Сотрудники
                </a>
            </li>
        </ul>
        <p class="menu-label">Производство</p>
        <ul class="menu-list">
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-cube"></i>
                    </span>
                    Компоненты
                </a>
            </li>
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-boxes-stacked"></i>
                    </span>
                    Изделия
                </a>
            </li>
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-truck-fast"></i>
                    </span>
                    Закупки
                </a>
            </li>
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-suitcase"></i>
                    </span>
                    Заказы
                </a>
            </li>
            <li>
                <a>
                    <span class="icon">
                        <i class="fas fa-warehouse"></i>
                    </span>
                    Склады
                </a>
            </li>
        </ul>
    </aside>
</template>

<style lang="scss">
    .logo {
        content: url("/logo.webp");
        max-height: 60px;
        position: relative;
        transform: translateX(-50%);
        left: 50%;
    }

    .menu-list a {
        padding-left: 0;
    }
</style>
