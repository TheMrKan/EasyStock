<template>
  <div class="app">
    <!-- Шапка -->
    <header>
      <nav>
        <router-link to="/">Главная</router-link> |
        <router-link to="/about">О нас</router-link>
      </nav>
    </header>

    <!-- Основной контент -->
    <main>
      <router-view /> <!-- Здесь будет подставляться контент страниц -->
    </main>

    <!-- Футер -->
    <footer>
      <p>© 2025 EasyStock</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LayoutDefault'
}
</script>
