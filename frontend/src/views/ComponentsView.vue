<script setup>
  import { useDataStore } from '@/stores/dataStore';
  import { fetchComponents } from "@/utils/components";
  import { ref } from 'vue';

  const dataStore = useDataStore();
  dataStore.title = 'Компоненты';
  dataStore.titleIcon = "fas fa-cube";

  const components = ref(null);

  loadComponents();

  async function loadComponents() {
    console.log("Fetching...");
    components.value = await fetchComponents();
    console.log("Fetched");
  }

</script>

<template>
  <div class="new-component">
    <span class="icon">
      <i class="fas fa-plus"></i>
    </span>
    Новый компонент
  </div>
  <div class="grid">
    <div v-if="components === null" class="loading-components">
      Загрузка...
    </div>
    <div v-else-if="components?.length === 0" class="no-components">
      Вы не добавили компоненты.
    </div>
    <div v-else v-for="comp in components" class="component-card">
      <img :src="comp.iconUrl" />
      <div class="component-data">
        <span class="component-name">{{ comp.name }}</span>
        <div class="component-controls">
          <router-link to="warehouses" class="component-available">
            <span class="icon">
              <i class="fas fa-warehouse"></i>
            </span>
            0 шт.
          </router-link>
          <router-link to="supplies" class="component-pending">
            <span class="icon">
              <i class="fas fa-truck-fast"></i>
            </span>
            0 шт.
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  @import '@/scss/globals.scss';

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
    gap: 0.5rem; // Расстояние между элементами
    width: 100%;
  }

  .new-component {
    $color: hsl($primary-hue, 60%, 50%);
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.3rem;
    font-size: 1rem;
    font-weight: 600;
    color: $color;
    border-radius: 10px;
    border: none;
    outline: 2px solid $color;
    background: none;
    cursor: pointer;
    text-align: center;

    &:hover {
      color: hsl($primary-hue, 80%, 50%);
      outline-color: hsl($primary-hue, 80%, 50%);
      box-shadow: hsla($primary-hue, 80%, 50%, 0.05) 0 0 10px 10px;
    }
  }

  .no-components, .loading-components {
    text-align: center;
    font-weight: 600;
    font-size: 1.2rem;
  }

  .component-card {
    min-width: 15rem;
    height: 5.5rem;
    background-color: hsla($primary-hue, 0%, 80%, 0.3);
    border-radius: 10px;
    padding: 0.5rem;
    display: flex;
    gap: 0.5rem;
    box-shadow: hsla($primary-hue, 30%, 0%, 0.1) 0 0 10px 5px;

    &:hover {
      outline: 2px solid hsla($primary-hue, 30%, 40%, 0.3);
      background-color: hsla($primary-hue, 0%, 70%, 0.2);
    }

    img {
      max-width: 25%;
    }

    .component-data {
      display: flex;
      flex-direction: column;

      .component-name {
        flex-grow: 1;
        line-height: 120%;
      }

      .component-controls {
        display: flex;
        flex-direction: row;
        gap: 0.7rem;


        a {
          color: hsl($primary-hue, 20%, 40%) !important;
          font-weight: 600;
        }
      }
    }
  }
</style>