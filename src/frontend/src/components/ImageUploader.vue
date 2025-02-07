<script setup lang="ts">
import { ref } from 'vue'
import heic2any from 'heic2any'

const acceptedFormats = ['image/jpeg', 'image/jpg', 'image/heic']
const previewUrl = ref(null)
const fileName = ref('')

const handleFile = async (file) => {
  if (!file || !acceptedFormats.includes(file.type)) {
    alert('JPEG または HEIC の画像を選択してください')
    return
  }

  fileName.value = file.name

  if (file.type === 'image/heic') {
    try {
      const convertedBlob = await heic2any({ blob: file, toType: 'image/jpeg' })
      previewUrl.value = URL.createObjectURL(convertedBlob)
    } catch (error) {
      console.error('HEIC 変換エラー:', error)
    }
  } else {
    previewUrl.value = URL.createObjectURL(file)
  }
}

const onFileChange = (event) => {
  const file = event.target.files[0]
  handleFile(file)
}
</script>

<template>
  <div class="container">
    <input id="fileInput" type="file" accept=".jpg,.jpeg,.heic" @change="onFileChange" hidden />
    <v-btn class="file-button" @click="document.getElementById('fileInput').click()">
      画像を選択
    </v-btn>
    <div v-if="previewUrl" class="preview-container">
      <img :src="previewUrl" alt="プレビュー画像" class="preview-image" />
      <p class="file-name">{{ fileName }}</p>
    </div>
  </div>
</template>

<style scoped>
.container {
  text-align: center;
  margin-top: 20px;
}

.file-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.file-button:hover {
  background-color: #0056b3;
}

.preview-container {
  margin-top: 20px;
  text-align: center;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 10px;
}

.file-name {
  font-size: 14px;
  color: #444;
  margin-top: 5px;
}
</style>
