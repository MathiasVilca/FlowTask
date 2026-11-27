import { Category } from './category.model';
export type TaskStatus = 'Pendiente' | 'En Progreso' | 'Completada';
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  due_date: string | null;
  category_id: number;

  category: Category;
}

export type TaskCreate = Omit<Task, 'id' | 'category'>;
export type TaskUpdate = Partial<TaskCreate>;
