import { Category } from "./category.model"
export type TaskStatus= 'Pendiente'|'En Progreso'|'Completada'
export interface Task {
    id:number;
    title:string;
    description:string|null;
    status: TaskStatus;
    due_date: string|null;
    category_id:number;

    category:Category;
};

export interface TaskCreate extends Omit<Task,"id"|"category"> {};
export interface TaskUpdate extends Partial<TaskCreate> {};