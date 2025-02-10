export interface UploadAgaveModel {
  name: string
  username: string
  username_source: string
  image_file: File
  image_file_path: string
  source: string
  sourcename: string
  image_source: string
  origin_country: string | null
  is_display: boolean
}
