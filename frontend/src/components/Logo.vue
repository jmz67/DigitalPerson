<template>
<div class="flex items-center">
    <div :class="['rounded-full mr-2', iconSizeClass, iconColorClass]"></div>
    <div :class="['font-bold', textSizeClass, textColorClass, textSpacingClass]">
    宁唐<span class="bg-gradient-to-r from-sky-600 to-sky-400 text-transparent bg-clip-text">健康</span>
    </div>
</div>
</template>

<script>
export default {
name: 'Logo',
props: {
    iconSizeClass: {
    type: String,
    default: 'w-10 h-10'
    },
    iconColorClass: {
    type: String,
    default: 'bg-blue-500'
    },
    textSizeClass: {
    type: String,
    default: 'text-2xl'
    },
    textColorClass: {
    type: String,
    default: 'text-gray-800'
    },
    textSpacingClass: {
    type: String,
    default: 'tracking-normal'
    }
}
}
</script>

<style scoped>
</style>