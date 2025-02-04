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
    .then((res: AxiosResponse<ProviderModel[]>) => {
      return sortList(res.data)
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

const sortList = (list: ProviderModel[]) => {
  return [...list].sort((a, b) => a.username.localeCompare(b.username, 'ja'))
}

export const getSearchListByProvider = async (provider: string): Promise<CardItemModel[]> => {
  return axios
    .get(`/api/search_provider?provider=${provider}`)
    .then((res: AxiosResponse<CardItemModel[]>) => {
      return sortListByName(res.data.map(transformCardItem))
    })
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

const sortListByName = (list: CardItemModel[]): CardItemModel[] => {
  return [...list].sort((a, b) => a.name.localeCompare(b.name, 'ja'))
}
