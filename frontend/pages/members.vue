<template>
  <div>
    <UContainer>
      <UPage>
        <UPageHeader
          title="Members"
          description="All members who signed up for the HackaCHazine"
        />

        <UPageBody>
          <UCard>
            <template #header>
              <div class="flex items-center justify-between gap-3">
                <UInput
                  v-model="search"
                  icon="i-heroicons-magnifying-glass-20-solid"
                  placeholder="Search..."
                />

                <div>
                  <UButton
                    @click="modalOpen = true"
                    icon="i-heroicons-user-plus-solid"
                  >
                    Add Member
                  </UButton>
                </div>
              </div>
            </template>

            <UTable
              :rows="filteredMembers"
              :columns="columns"
              :sort="sort"
              :loading="pending"
            />
          </UCard>
        </UPageBody>
      </UPage>
    </UContainer>

    <ModalUserCreate v-model:open="modalOpen" @created="refresh" />
  </div>
</template>

<script setup lang="ts">
const search = useState(() => "");
const modalOpen = ref(false);

const sort = ref({
  column: "name",
  direction: "asc" as const,
});

const columns = [
  {
    label: "ID",
    key: "id",
  },
  {
    label: "Name",
    key: "name",
    sortable: true,
  },
  {
    label: "Address",
    key: "address.fullName",
  },
];

const { data: members, pending, refresh } = await useFetch("/api/member");

const filteredMembers = computed(() =>
  members.value?.filter((member) =>
    member.name.toLowerCase().includes(search.value.toLowerCase())
  )
);
</script>
