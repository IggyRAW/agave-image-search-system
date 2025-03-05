<script setup lang="ts">
import { ref } from 'vue'
import type { CardItemModel } from '../api/search'
import { useSearchStore } from '@/stores/searchStore'
defineProps<{ item: CardItemModel }>()

const searchStore = useSearchStore()
const isActive = ref(false)
const show = ref(false)
const showFeature = ref(false)
const dialog = ref(false)
const selectedImage = ref('')

const openDialog = (item: CardItemModel) => {
  selectedImage.value = '/api/' + item.image_file_path
  dialog.value = true
}

// 検索処理
const onSearch = (searchWord: string) => {
  searchStore.setSearchWord(searchWord)
  searchStore.setSearchType(1)
  searchStore.fetchSearchList()

  searchStore.scrollToTop()
}

const onFeature = async (searchWord: string) => {
  await searchStore.fetchFeature(searchWord)
  showFeature.value = true
}
</script>

<template>
  <v-card class="mx-auto width: 100%" max-width="344">
    <!-- 画像をカードいっぱいに表示 -->
    <v-img
      :src="'/api/' + item.image_file_path"
      :alt="item.name"
      class="responsive-img"
      cover
      @click="openDialog(item)"
      lazy
    ></v-img>

    <v-card-title
      class="responsive-title"
      @click="onSearch(item.name)"
      :class="{ active: isActive }"
      @touchstart="isActive = true"
      @touchend="isActive = false"
      >アガベ {{ item.name }}</v-card-title
    >

    <v-card-subtitle>
      提供者：<a :href="item.image_source" target="_blank" rel="noopener noreferrer">
        {{ item.username }}
      </a>
    </v-card-subtitle>

    <v-card-actions class="d-flex justify-end">
      <v-btn
        variant="text"
        color="green-darken-4"
        text="特徴"
        @click="onFeature(item.name)"
      ></v-btn>
      <v-spacer></v-spacer>
      <v-btn :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="show = !show"></v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider></v-divider>
        <v-card-text>
          <template v-if="item.username !== item.source">
            購入元：<a :href="item.sourcename" target="_blank" rel="noopener noreferrer">
              {{ item.source }}
            </a>
            <br />
          </template>
          <template v-if="item.origin_country !== '不明'">
            原産国：{{ item.origin_country }}
            <br />
          </template>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>

  <!-- モーダル表示 -->
  <v-dialog v-model="dialog" max-width="800px">
    <v-img :src="selectedImage" alt="404 Error" max-height="600px" lazy></v-img>
  </v-dialog>
  <v-dialog v-model="showFeature" max-width="800px" class="d-flex justify-center align-center">
    <v-card class="w-100 d-flex flex-column" style="max-height: 90vh">
      <v-card-text class="pb-16 flex-grow-1 overflow-y-auto" style="max-height: 80vh">
        <p class="text-h6">{{ item.name }}</p>
        <p>{{ searchStore.feature }}</p>
      </v-card-text>
      <v-card-actions
        class="pt-0 position-absolute w-100"
        style="bottom: 0; left: 0; background: white"
      >
        <v-btn
          color="grey-darken-1"
          text="CLOSE"
          variant="text"
          @click="showFeature = false"
        ></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@font-face {
  font-family: 'MyCustomFont';
  src:
    url('path/to/font.woff2') format('woff2'),
    url('path/to/font.woff') format('woff');
  font-display: swap;
}

.responsive-title {
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
  font-size: clamp(12px, 2vw, 18px);
  line-height: 1.2;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.responsive-title.active {
  background-color: rgba(0, 17, 1, 0.301);
}

.v-img {
  object-fit: cover;
}

.responsive-img {
  height: clamp(200px, 30vw, 300px);
}
</style>
