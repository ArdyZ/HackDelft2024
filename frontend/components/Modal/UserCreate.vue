<template>
  <UModal v-model="open">
    <UForm
      ref="form"
      :schema="memberCreate"
      :state="state"
      class="space-y-4"
      @submit="create"
    >
      <UCard
        :ui="{
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

        <UFormGroup label="Name" name="name">
          <UInput v-model="state.name" />
        </UFormGroup>

        <template #footer>
          <div class="flex justify-end">
            <UButton type="submit" size="md">Create</UButton>
          </div>
        </template>
      </UCard>
    </UForm>
  </UModal>
</template>

<script setup lang="ts">
import type { FormSubmitEvent } from "#ui/types";

import { create as memberCreate } from "../../schema/member";

const open = defineModel<boolean>("open");
const emit = defineEmits<{ created: [] }>();

const toast = useToast();

const form = ref();
const state = reactive<memberCreate>({
  name: "",
});

const globalErrors = computed(
  () =>
    form?.value && form.value.getErrors("global").map((err: any) => err.message)
);

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
