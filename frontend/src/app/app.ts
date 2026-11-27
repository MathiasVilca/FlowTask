import { Component, signal,OnInit,inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CategoryService } from './services/category';
import { TaskService } from './services/task';
import { Task } from './models/task.model';
import { switchMap, tap } from 'rxjs';
import { TaskCard } from './components/task-card/task-card';

@Component({
  imports: [RouterOutlet,TaskCard],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App implements OnInit {
  private categoryService = inject(CategoryService);
  private taskService = inject(TaskService);
  protected readonly title = signal('frontend');

  ngOnInit(): void {
    this.categoryService.getCategories().subscribe((cats) => console.log('Categorías:', cats));
    this.taskService.loadTasks().subscribe((tasks) => console.log('Tareas:', tasks));
  }

  sampleTask: Task = {
    id: 1,
    title: 'Preparar arquitectura del frontend',
    description: 'Configurar componentes standalone, servicios HTTP y Tailwind CSS.',
    status: 'En Progreso',
    due_date: '2026-11-30',
    category_id: 1,
    category: { id: 1, name: 'Desarrollo', description: null },
  };
}

