import axios, { AxiosError, type AxiosResponse } from 'axios'
import { INSTAGRAMURL } from '@/environment'

export interface CardItemModel {
  id: string
  name: string
  username: string
  username_source: string
  image_file_path: string
  source: string
  sourcename: string
  image_source: string
  origin_country: string
}

export const getSearchList = async (
  search_word: string,
  page: number = 1,
  limit: number = 18,
): Promise<{ total: number; search_list: CardItemModel[] }> => {
  return axios
    .get(`/api/search?search_word=${search_word}&page=${page}&limit=${limit}`)
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

export const transformCardItem = (cardItem: CardItemModel): CardItemModel => {
  return {
    ...cardItem,
    username_source: `${INSTAGRAMURL}${cardItem.username_source}`,
    image_source: `${INSTAGRAMURL}/p/${cardItem.image_source}`,
    sourcename: `${INSTAGRAMURL}${cardItem.sourcename}`,
  }
}
