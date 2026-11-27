import { Component, inject, OnInit } from '@angular/core';
import { TaskService } from '../../services/task';
import { CategoryService } from '../../services/category';
import { Task,TaskStatus } from '../../models/task.model';
import { TaskCard } from '../task-card/task-card';
import { TaskForm } from '../task-form/task-form';
import { AsyncPipe } from '@angular/common';

@Component({
  imports: [AsyncPipe, TaskCard,TaskForm],
  standalone: true,
  selector: 'app-task-list',
  styleUrl: './task-list.css',
  templateUrl: './task-list.html',
})
export class TaskList implements OnInit {
  private readonly taskService = inject(TaskService);
  private readonly categoryService = inject(CategoryService);
  readonly tasks$ = this.taskService.tasks$;
  readonly categories$ = this.categoryService.getCategories();
  selectedStatus?: TaskStatus;
  selectedCategoryId?: number;
  isFormOpen = false;
  selectedTaskToEdit: Task | null = null;

  ngOnInit(): void {
    this.taskService.loadTasks().subscribe();
  }

  openCreateForm():void{
    this.selectedTaskToEdit= null;
    this.isFormOpen= true;
  }

  openEditForm(task:Task):void{
    this.selectedTaskToEdit = task;
    this.isFormOpen= true;
  }

  closeForm():void{
    this.selectedTaskToEdit= null;
    this.isFormOpen= false;
  }

  handleTaskSaved():void{
    this.closeForm();
    this.applyFilters();
  }

  onStatusFilterChange(event:Event): void{
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.selectedStatus = selectedValue ? (selectedValue as TaskStatus) : undefined;
    this.applyFilters();
  }

  onCategoryFilterChange(event: Event): void {
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.selectedCategoryId = selectedValue ? Number(selectedValue) : undefined;
    this.applyFilters();
  }

  handleCompleteTask(id:number):void{
    this.taskService.updateTask(id,{'status':'Completada'}).subscribe({
      next: () => this.applyFilters(),
    });
  }

  handleDeleteTask(id:number):void{
    const confirmed = window.confirm("Estas seguro que quieres eliminar esta tarea?");
    if (!confirmed) return;
    this.taskService.deleteTask(id).subscribe({
      next: () => this.applyFilters(),
    });
  }

  private applyFilters(): void {
    this.taskService.loadTasks(this.selectedStatus, this.selectedCategoryId).subscribe();
  }
}
