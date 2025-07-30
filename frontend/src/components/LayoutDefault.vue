<script>
import LeftMenu from './LeftMenu.vue';

export default {
  components: {
    LeftMenu
  }
};
</script>

<template>
    <div class="root">
        <div class="main-column">
            <div class="box">

            </div>
        </div>
        <div class="menu-column">
            <div class="box">
                <LeftMenu/>
            </div>
        </div>
    </div>

</template>

<style scoped lang="scss">

    $primary-hue: 232;
    $--bulma-primary: hsl($primary-hue, 63%, 33%);

    $main-column-width: 650px;
    $menu-column-width: 225px;
    $menu-column-margin-from-center: calc($main-column-width / 2) + calc($menu-column-width / 2);
    $menu-column-margin: calc(50vw - $menu-column-margin-from-center);

        .content-column {
            height: 100%;
            position: absolute;
            padding-top: 10px;
            padding-bottom: 10px;
            padding-right: 8px;
            padding-left: 8px;

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
        }

        .menu-column {
            @extend .content-column;
            width: $menu-column-width;
            transform: translate(-50%, 0);
            left: $menu-column-margin;
        }

        .root {
            background-image: url('/bg.webp');
            background-position: center center;
            background-repeat: no-repeat;
            background-size: cover;
            height: 100vh;
            width: 100vw;
        }


    </style>
