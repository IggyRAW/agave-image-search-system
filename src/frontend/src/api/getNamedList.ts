import axios, { AxiosError, type AxiosResponse } from 'axios'

export interface NamedModel {
  name: string
}

export const getNamedList = async (): Promise<NamedModel[]> => {
  return axios
    .get(`/api/get/named/list`)
    .then((res: AxiosResponse<NamedModel[]>) => res.data)
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
