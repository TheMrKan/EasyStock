<script setup>
    import { useDataStore } from '@/stores/dataStore';

    const dataStore = useDataStore();
    dataStore.title = 'Обзор';
    dataStore.titleIcon = "fas fa-chart-bar";
</script>

<template>
    <section>
        <h1>Домашняя страницы</h1>
        <p>Контент домашней страницы</p>
    </section>
</template>