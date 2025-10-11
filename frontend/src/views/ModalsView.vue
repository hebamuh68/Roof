<template>
<div class="modals">
<h1>Modals</h1>
<button @click="showModal = true">Show modal</button>
<Modal
  v-if="showModal"
  title="My modal title (via prop)"
  @close="showModal = false"
>
  <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Beatae ipsa laboriosam vero natus ut rerum quaerat, saepe praesentium tempore et hic velit odio nemo minus labore quam ullam quod architecto?</p>
</Modal>
</div>
</template>

<script setup>
  import { ref } from 'vue'
  import Modal from '@/components/Modal.vue'
  const showModal = ref(false)

</script>

<style scoped>
.modals {
  padding: 20px;
}
</style>