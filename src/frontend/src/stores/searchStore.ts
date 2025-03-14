import { getSearchList, type CardItemModel } from '@/api/search'
import { getSearchListByNamed, type NamedModel } from '@/api/getNamedList'
import { defineStore } from 'pinia'
import { getSearchListByProvider } from '@/api/getProviders'
import { initItem } from '@/api/types/initItem'
import { initialized } from '@/api/init'
import { getFeature, getSimilerSearch } from '@/api/getFeature'
import { type FeatureModel } from '@/api/types/feature'

export const useSearchStore = defineStore('search', {
  state: () => ({
    searchWord: '',
    searchType: 0, // 0:標準検索 1:ネームド検索 2:提供者検索 3:類似度検索
    currentPage: 1,
    totalPage: 0,
    limit: 18,
    searchList: initItem as CardItemModel[],
    namedList: [] as NamedModel[],
    rankingList: [] as string[],
    feature: {} as FeatureModel,
    activeFeature: null as number | null,
    lastSimilerName: '' as string,
  }),

  actions: {
    setSearchWord(word: string) {
      this.searchWord = word
      this.currentPage = 1
    },

    setSearchType(type: number) {
      this.searchType = type
    },

    setTotalPage(totalPage: number) {
      this.totalPage = totalPage
    },

    async fetchRankingList() {
      try {
        this.rankingList = await initialized()
      } catch (err) {
        console.error('ランキングリストの取得に失敗しました', err)
      }
    },

    async fetchSearchList() {
      try {
        console.log(`検索ワード: ${this.searchWord}, ページ: ${this.currentPage}`)
        this.activeFeature = null

        let data
        if (this.searchType === 0) {
          // 標準検索
          data = await getSearchList(this.searchWord, this.currentPage, this.limit)
        } else if (this.searchType === 1) {
          // ネームド検索
          data = await getSearchListByNamed(this.searchWord, this.currentPage, this.limit)
        } else if (this.searchType === 2) {
          // 提供者検索
          data = await getSearchListByProvider(this.searchWord, this.currentPage, this.limit)
        } else {
          // 類似検索
          this.lastSimilerName = this.feature.name
          data = await getSimilerSearch(this.feature, this.currentPage, this.limit)
        }

        // トータルページ数の計算
        this.totalPage = Math.ceil(data.total / this.limit)

        // 検索結果リストの反映
        this.searchList = data.search_list
      } catch (error) {
        console.error('検索エラー：', error)
      }
    },

    nextPage() {
      this.fetchSearchList()
    },

    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    toggleFeature(index: number) {
      this.activeFeature = this.activeFeature === index ? null : index
    },

    async fetchFeature(searchWord: string) {
      try {
        this.feature = await getFeature(searchWord)
      } catch (err) {
        console.error('エラー', err)
      }
    },
  },
})
