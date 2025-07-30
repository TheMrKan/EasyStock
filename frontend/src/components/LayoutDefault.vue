<script setup>
    import LeftMenu from './LeftMenu.vue';
    import { ref, onMounted, onUnmounted } from 'vue';
    import { useDataStore } from '@/stores/dataStore';
    

    const isMenuVisible = ref(true);
    const menuBreakpoint = 748;

    const dataStore = useDataStore();

    const handleResize = () => {
        isMenuVisible.value = window.innerWidth >= menuBreakpoint;
    };

    onMounted(() => {
        window.addEventListener('resize', handleResize);
        handleResize();
    });

    onUnmounted(() => {
        window.removeEventListener('resize', handleResize);
    });


</script>

<template>
    <div class="root">
        <div class="main-column">
            <div class="box">
                <div class="header">
                    <div class="left">
                        <button class="button menu-button" v-show="!isMenuVisible">
                            <span class="icon is-large">
                                <i class="fas fa-bars fa-lg"></i>
                            </span>
                        </button>
                    </div>
                    <div class="center">
                        <h1 class="title is-4">
                            <span class="icon" style="margin-right: 5px;">
                                <i :class="dataStore.titleIcon"></i>
                            </span>
                            {{ dataStore.title }}
                        </h1>
                    </div>
                    <div class="right"></div>
                </div>
                <router-view />
            </div>
        </div>
        <div class="menu-column" v-show="isMenuVisible">
            <div class="box">
                <LeftMenu />
            </div>
        </div>
    </div>

</template>

<style scoped lang="scss">
    @import '@/scss/global.scss';

    $--bulma-primary: hsl($primary-hue, 63%, 33%);

    $main-column-width: 40vw;
    $menu-column-width: 225px;
    $menu-column-margin: calc(50vw - calc(calc($main-column-width / 2) + calc($menu-column-width / 2)));

    .root {
        background-image: url('/bg.webp');
        background-position: center center;
        background-repeat: no-repeat;
        background-size: cover;
        height: 100vh;
        width: 100vw;
    }

    .content-column {
        height: 100%;
        position: absolute;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-right: 8px;
        padding-left: 8px;

        @include fullScreen {
            padding: 0;
        }

        >.box {
            height: 100%;
            border-radius: 15px;
            border-width: 3px;
            border-style: solid;
            border-color: hsla($primary-hue, 30%, 40%, 1);
            box-shadow: hsla($primary-hue, 30%, 0%, 0.6) 0 0 20px 5px;
            background-color: hsla($primary-hue, 2%, 70%, 0.7);
            backdrop-filter: blur(5px);
        }
    }

    .main-column {
        @extend .content-column;
        width: $main-column-width;
        transform: translate(-50%, 0);
        left: 50%;

        @include menuBreakpoint {
            width: 80vw;
        }

        @include fullScreen {
            width: 100%;

            >.box {
                border-radius: 0;
            }
        }
    }

    .menu-column {
        @extend .content-column;
        width: $menu-column-width;
        transform: translate(-50%, 0);
        left: $menu-column-margin;
    }

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-bottom: 1.5em;

        >.left {
            width: 10%;
        }

        >.center {
            width: 80%;
            display: flex;
            justify-content: center;
        }

        >.right {
            width: 10%;
        }

        .menu-button {
            background: none;
            border: none;
        }
    }

</style>
