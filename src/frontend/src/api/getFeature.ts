import axios, { AxiosError, type AxiosResponse } from 'axios'
import { type FeatureModel } from './types/feature'
import { transformCardItem, type CardItemModel } from './search'

export const getFeature = async (search_word: string): Promise<FeatureModel> => {
  return axios
    .get(`/api/get/feature?search_word=${search_word}`)
    .then((res: AxiosResponse<FeatureModel>) => {
      if (!res.data) {
        return getDefaultFeatureModel(search_word)
      }
      return res.data
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

function getDefaultFeatureModel(search_word: string): FeatureModel {
  return {
    name: search_word,
    leaf_color: '',
    leaf_type: '',
    spine_color: '',
    spine_type: [],
  }
}

export const getSimilerSearch = async (
  feature: FeatureModel,
  page: number = 1,
  limit: number = 18,
): Promise<{ total: number; search_list: CardItemModel[] }> => {
  return axios
    .get('/api/get/similer_search', {
      params: {
        feature: JSON.stringify(feature),
        page: page,
        limit: limit,
      },
    })
    .then((res: AxiosResponse<{ total: number; search_list: CardItemModel[] }>) => {
      return {
        total: res.data.total,
        search_list: res.data.search_list.map(transformCardItem),
      }
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
