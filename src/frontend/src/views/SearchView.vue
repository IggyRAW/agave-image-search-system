<script setup lang="ts">
import { ref } from 'vue'

import Header from '../components/organisms/Header.vue'
import SearchBar from '@/components/SearchBar.vue'
import CardItem from '@/components/CardItem.vue'
import type { CardItemModel } from '../api/search'

// データ受け取り
const receivedSearchList = ref<CardItemModel[]>([])

const handleSearchList = (list: CardItemModel[]) => {
  receivedSearchList.value = list
}
</script>

<template>
  <v-app>
    <Header @searchList="handleSearchList" />
    <v-main>
      <SearchBar @searchList="handleSearchList" />
      <div style="max-width: 95%; margin: 0 auto; padding: 16px">
        <v-row>
          <v-col
            v-for="item in receivedSearchList"
            :key="item.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
            xl="2"
          >
            <CardItem :item="item" />
          </v-col>
        </v-row>
      </div>
    </v-main>
  </v-app>
</template>
