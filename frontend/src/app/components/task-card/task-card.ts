import { Component, input } from '@angular/core';
import { Task,TaskStatus } from '../../models/task.model';

@Component({
  imports: [],
  selector: 'app-task-card',
  styleUrl: './task-card.css',
  templateUrl: './task-card.html',
})
export class TaskCard {
  task= input.required<Task>()
  
  getStatusClasses(status: TaskStatus): string {
    const base = "rounded-full px-2.5 py-0.5 text-xs whitespace-nowrap"
    const colors: Record<TaskStatus, string> = {
      'Pendiente': 'bg-red-100 text-red-700',
      'En Progreso': 'bg-amber-100 text-amber-800',
      'Completada': 'bg-emerald-100 text-emerald-700',
    };
    return `${base} ${colors[status]}`;
  }
}
