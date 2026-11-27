import { Component, inject, OnInit } from '@angular/core';
import { TaskService } from '../../services/task';
import { CategoryService } from '../../services/category';
import { TaskStatus } from '../../models/task.model';
import { TaskCard } from '../task-card/task-card';
import { AsyncPipe } from '@angular/common';

@Component({
  imports: [AsyncPipe, TaskCard],
  standalone: true,
  selector: 'app-task-list',
  styleUrl: './task-list.css',
  templateUrl: './task-list.html',
})
export class TaskList implements OnInit {
  private taskService = inject(TaskService);
  private readonly categoryService = inject(CategoryService);
  readonly tasks$ = this.taskService.tasks$;
  readonly categories$ = this.categoryService.getCategories();
  selectedStatus?: TaskStatus;
  selectedCategoryId?: number;

  ngOnInit(): void {
    this.taskService.loadTasks().subscribe();
  }

  onStatusFilterChange(event:Event){
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.selectedStatus = selectedValue ? (selectedValue as TaskStatus) : undefined;
    this.applyFilters();
  }

  onCategoryFilterChange(event: Event): void {
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.selectedCategoryId = selectedValue ? Number(selectedValue) : undefined;
    this.applyFilters();
  }

  private applyFilters(): void {
    this.taskService.loadTasks(this.selectedStatus, this.selectedCategoryId).subscribe();
  }
}
