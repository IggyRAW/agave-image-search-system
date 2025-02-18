import axios, { AxiosError, type AxiosResponse } from 'axios'

interface InitResponse {
  ranking_list: string[]
}

// rankingリストの作成
export const initialized = async (): Promise<string[]> => {
  return axios
    .get(`/api/init`)
    .then((res: AxiosResponse<InitResponse>) => {
      return res.data.ranking_list
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
