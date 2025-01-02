import axios, { AxiosError, type AxiosResponse } from 'axios'
import { INSTAGRAMURL } from '@/environment'

export interface ProviderModel {
  username: string
}

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

export const getProviders = async (): Promise<ProviderModel[]> => {
  return axios
    .get(`/api/get/providers`)
    .then((res: AxiosResponse<ProviderModel[]>) => res.data)
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

export const getSearchList = async (provider: string): Promise<CardItemModel[]> => {
  return axios
    .get(`/api/search_provider?provider=${provider}`)
    .then((res: AxiosResponse<CardItemModel[]>) => res.data.map(transformCardItem))
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

const transformCardItem = (cardItem: CardItemModel): CardItemModel => {
  return {
    ...cardItem,
    username_source: `${INSTAGRAMURL}${cardItem.username_source}`,
    image_source: `${INSTAGRAMURL}/p/${cardItem.image_source}`,
    sourcename: `${INSTAGRAMURL}${cardItem.sourcename}`,
  }
}
