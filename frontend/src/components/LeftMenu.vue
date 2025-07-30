<template>
    <aside class="menu">
        <img class="logo is-centered"></img>
        <p class="menu-label">ОБЩЕЕ</p>
        <ul class="menu-list">
            <li>
                <router-link to="/">
                    <span class="icon">
                        <i class="fas fa-chart-bar"></i>
                    </span>
                    Обзор
                </router-link>
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
                <router-link to="components">
                    <span class="icon">
                        <i class="fas fa-cube"></i>
                    </span>
                    Компоненты
                </router-link>
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
    @import '@/scss/global.scss';

    .logo {
        content: url("/logo.webp");
        max-height: 60px;
        position: relative;
        transform: translateX(-50%);
        left: 50%;
    }

    .menu-list a {
        padding-left: 0;
        border-radius: 8px !important;

        &:hover {
            background-color: hsla($primary-hue, 63%, 70%, 0.2);
        }
    }

    .router-link-exact-active {
        font-weight: bold;
        background-color: hsla($primary-hue, 63%, 50%, 0.2) !important;

    }
</style>
