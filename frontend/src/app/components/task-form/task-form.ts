import { Component, effect,inject, input,output } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CategoryService } from '../../services/category';
import { TaskService } from '../../services/task';
import { Task,TaskStatus } from '../../models/task.model';

@Component({
  imports: [ReactiveFormsModule, AsyncPipe],
  selector: 'app-task-form',
  styleUrl: './task-form.css',
  templateUrl: './task-form.html',
})
export class TaskForm {
  private readonly fb = inject(FormBuilder)
  private readonly taskService = inject(TaskService)
  private readonly categoryService = inject(CategoryService)

  readonly categories$ = this.categoryService.getCategories()

  taskToEdit= input<Task | null>(null); //Se deja en nulo si es para creación
  saved = output<void>(); //Se guardó correctamente
  cancelled = output<void>(); //Se canceló

  readonly taskForm= this.fb.nonNullable.group({
    title: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(150), Validators.pattern(/\S/)]],
    description: ['',[Validators.maxLength(100)]],
    status: ['Pendiente' as TaskStatus, [Validators.required]],
    due_date: [''],
    category_id: [null as number | null, [Validators.required]], 
  })

  constructor() {
    effect(() => {
      const task = this.taskToEdit();
      if (task) {
        this.taskForm.patchValue({
          title: task.title,
          description: task.description ?? '',
          status: task.status,
          due_date: task.due_date ?? '',
          category_id: task.category.id,
        });
      } else {
        this.taskForm.reset({
          title: '',
          description: '',
          status: 'Pendiente',
          due_date: '',
          category_id: null,
        });
      }
    });
  }

  onSubmit(): void {
    if (this.taskForm.invalid){ //Verficación de validaciones
      this.taskForm.markAllAsTouched();
      return;
    }

    const rawValue = this.taskForm.getRawValue(); //Preparar y limpiar datos para app
    const payload = {
      title: rawValue.title.trim(),
      description: rawValue.description.trim() || null,
      status: rawValue.status,
      due_date: rawValue.due_date || null,
      category_id: Number(rawValue.category_id),
    };

    const currentTask = this.taskToEdit(); //Selección entre editar o crear

    if (currentTask) {
      this.taskService.updateTask(currentTask.id, payload).subscribe({
        next: () => this.saved.emit(),
      });
    } else {
      this.taskService.createTask(payload).subscribe({
        next: () => this.saved.emit(),
      });
    }
  }

  onCancel(): void {
    this.cancelled.emit();
  }
}
