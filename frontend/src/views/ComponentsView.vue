<script setup>
  import { useDataStore } from '@/stores/dataStore';

  const dataStore = useDataStore();
  dataStore.title = 'Компоненты';
  dataStore.titleIcon = "fas fa-cube";
</script>

<template>
  <section>
    <h1>Главная страница</h1>
    <p>Это контент, который отображается внутри LayoutDefault.</p>
  </section>
</template>
