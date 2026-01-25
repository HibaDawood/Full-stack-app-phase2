// translations/zh.ts
import { TranslationKeys } from '../types/i18n';

export const zh: TranslationKeys = {
  // Common
  appTitle: '待办事项应用',
  welcome: '欢迎',
  loading: '加载中...',
  error: '错误',
  save: '保存',
  cancel: '取消',
  delete: '删除',
  edit: '编辑',
  create: '创建',
  search: '搜索',
  filter: '筛选',
  reset: '重置',
  language: '语言',

  // Authentication
  signIn: '登录',
  signUp: '注册',
  signOut: '退出登录',
  email: '邮箱',
  password: '密码',
  confirmPassword: '确认密码',
  alreadyHaveAccount: '已有账户？',
  dontHaveAccount: '没有账户？',
  createAccount: '创建账户开始使用',
  welcomeBack: '欢迎回来！',
  signInToAccount: '请登录您的账户',
  passwordMinLength: '密码长度至少为8个字符',
  passwordsMatch: '两次输入的密码不一致',
  validEmail: '请输入有效的邮箱地址',

  // Tasks
  yourTasks: '我的任务',
  allTasks: '所有任务',
  pendingTasks: '待处理任务',
  inProgress: '进行中',
  completedTasks: '已完成任务',
  noTasks: '没有找到任务。创建您的第一个任务！',
  noPending: '没有待处理的任务',
  noInProgress: '没有进行中的任务',
  noCompleted: '暂无已完成任务',
  createFirstTask: '创建您的第一个任务！',
  taskTitle: '任务标题',
  taskDescription: '描述',
  taskStatus: '状态',
  deleteConfirmation: '您确定要删除此任务吗？',

  // Status options
  statusAll: '全部任务',
  statusPending: '待处理',
  statusInProgress: '进行中',
  statusCompleted: '已完成',

  // Filters
  filterByStatus: '按状态筛选',
  searchPlaceholder: '按标题或描述搜索...',
};