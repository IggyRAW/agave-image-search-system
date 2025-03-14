<script setup lang="ts">
import { ref, computed } from 'vue'
import type { CardItemModel } from '../api/search'
import { useSearchStore } from '@/stores/searchStore'

const props = defineProps<{ item: CardItemModel; index: number }>()

const searchStore = useSearchStore()
const isActive = ref(false)
const showFeature = computed(() => searchStore.activeFeature === props.index)
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

// 特徴データ取得
const onFeature = async (item: CardItemModel) => {
  searchStore.toggleFeature(props.index)
  await searchStore.fetchFeature(item.name)
}

// 類似検索
const onSimilerSearch = async () => {
  searchStore.setSearchType(3)
  await searchStore.fetchSearchList()
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
      <v-spacer></v-spacer>
      <v-btn
        :icon="showFeature ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        @click="onFeature(item)"
      ></v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="showFeature">
        <v-divider></v-divider>
        <v-card-text>
          <p>
            葉色：{{
              searchStore.feature?.leaf_color?.length ? searchStore.feature.leaf_color : '情報なし'
            }}
          </p>
          <p>
            葉形：{{
              searchStore.feature?.leaf_type?.length ? searchStore.feature.leaf_type : '情報なし'
            }}
          </p>
          <p>
            鋸歯色：{{
              searchStore.feature?.spine_color?.length
                ? searchStore.feature.spine_color
                : '情報なし'
            }}
          </p>
          <p>
            鋸歯タイプ：
            {{
              searchStore.feature?.spine_type?.length
                ? searchStore.feature.spine_type.join(', ')
                : '情報なし'
            }}
          </p>
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
          <div class="text-end">
            <v-btn
              class="justify-center"
              variant="text"
              color="green-darken-4"
              @click="onSimilerSearch"
              >似てるアガベを検索</v-btn
            >
          </div>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>

  <!-- モーダル表示 -->
  <v-dialog v-model="dialog" max-width="800px">
    <v-img :src="selectedImage" alt="404 Error" max-height="600px" lazy></v-img>
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
