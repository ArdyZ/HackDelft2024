<template>
  <LMap style="height: 350px" :zoom="6" :center="[47.21322, -1.559482]">
    <LTileLayer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      layer-type="base"
      name="OpenStreetMap"
    />
  </LMap>
</template>
