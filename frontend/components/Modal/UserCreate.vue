<template>
  <USlideover v-model="open">
    <UForm
      ref="form"
      :schema="memberCreate"
      :state="state"
      class="space-y-4"
      @submit="create"
    >
      <UCard
        class="flex flex-col flex-1"
        :ui="{
          body: { base: 'flex-1' },
          ring: '',
          divide: 'divide-y divide-gray-100 dark:divide-gray-800',
        }"
      >
        <template #header>
          <div class="flex items-center justify-between">
            <h3
              class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
            >
              Add A Member
            </h3>

            <UButton
              color="gray"
              variant="ghost"
              icon="i-heroicons-x-mark-20-solid"
              class="-my-1"
              @click="open = false"
            />
          </div>
        </template>

        <UAlert
          v-for="err in globalErrors"
          color="red"
          variant="solid"
          class="mb-4"
          :description="err"
        />

        <UFormGroup label="Name" name="name" class="mb-2">
          <UInput v-model="state.name" />
        </UFormGroup>

        <UFormGroup label="Address" name="address" class="mb-2">
          <USelectMenu
            v-model="state.address"
            :loading="addressLoading"
            :searchable="searchAddress"
            option-attribute="fullAddress"
            searchable-placeholder="Search an Address..."
            :uiMenu="{ container: 'z-[9999] group' }"
          />
        </UFormGroup>

        <div class="h-64 mt-4">
          <LMap
            :zoom="14"
            :center="
              state.address
                ? [state.address.coordinates[1], state.address.coordinates[0]]
                : [51.998752, 4.373719]
            "
            ref="map"
          >
            <LTileLayer
              url="https://tile.openstreetmap.de/{z}/{x}/{y}.png"
              attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
              layer-type="base"
              name="OpenStreetMap"
            />
            <LMarker
              v-if="state.address"
              :lat-lng="[
                state.address.coordinates[1],
                state.address.coordinates[0],
              ]"
            >
              <LTooltip>{{ state.address.name }}</LTooltip>
            </LMarker>
          </LMap>
        </div>

        <template #footer>
          <div class="flex justify-end">
            <UButton type="submit" size="md">Create</UButton>
          </div>
        </template>
      </UCard>
    </UForm>
  </USlideover>
</template>

<script setup lang="ts">
import type { FormSubmitEvent } from "#ui/types";

import { create as memberCreate } from "../../server/lib/validation/member";

const open = defineModel<boolean>("open");
const emit = defineEmits<{ created: [] }>();

const toast = useToast();

const form = ref();
const addressLoading = ref(false);
const state = reactive<memberCreate>({
  name: "",
  address: null as any,
});

const globalErrors = computed(
  () =>
    form?.value && form.value.getErrors("global").map((err: any) => err.message)
);

const searchAddress = async (q: string) => {
  addressLoading.value = true;
  const addresses = await $fetch("/api/geocode", {
    params: { q },
  });
  addressLoading.value = false;

  return addresses;
};

const create = async (e: FormSubmitEvent<memberCreate>) => {
  form.value.clear();
  try {
    const res = await $fetch("/api/member", {
      method: "post",
      body: e.data,
    });

    toast.add({
      title: "Member added",
      description: `'${e.data.name}' has been added.`,
    });
    state.name = "";
    state.address = null as any;

    open.value = false;
    emit("created");
  } catch (err: any) {
    if (err.data.errors) {
      form.value.setErrors(
        err.data.errors.map((err: any) => ({
          message: err.message,
          path: err.path,
        }))
      );
    }

    form.value.setErrors([{ message: err.data.message, path: "global" }]);
  }
};
</script>
