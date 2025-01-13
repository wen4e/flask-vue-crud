<template>
  <div class="container">
    <div class="row">
      <el-upload ref="upload" class="upload-demo" action="http://localhost:5001/upload/excel" :file-list="fileList" :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload" :on-exceed="handleExceed" :limit="1" accept=".xlsx,.xls">
        <el-button type="primary">上传Excel文件</el-button>
        <template #tip>
          <div class="el-upload__tip">请上传 xlsx 或 xls 格式的Excel文件</div>
        </template>
      </el-upload>
      <el-table :data="trData" style="width: 100%">
        <el-table-column prop="trName" label="交易名称" />
        <el-table-column prop="trCode" label="交易码" />
        <el-table-column label="操作">
          <template #default>
            <el-button link type="primary" size="small" @click="handleClick"> Detail </el-button>
            <el-button link type="primary" size="small">Edit</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- add new book modal -->
    <div ref="addBookModal" class="modal fade" :class="{ show: activeAddBookModal, 'd-block': activeAddBookModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new book</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleAddBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addBookTitle" class="form-label">Title:</label>
                <input type="text" class="form-control" id="addBookTitle" v-model="addBookForm.title" placeholder="Enter title" />
              </div>
              <div class="mb-3">
                <label for="addBookAuthor" class="form-label">Author:</label>
                <input type="text" class="form-control" id="addBookAuthor" v-model="addBookForm.author" placeholder="Enter author" />
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="addBookRead" v-model="addBookForm.read" />
                <label class="form-check-label" for="addBookRead">Read?</label>
              </div>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary btn-sm" @click="handleAddSubmit">Submit</button>
                <button type="button" class="btn btn-danger btn-sm" @click="handleAddReset">Reset</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddBookModal" class="modal-backdrop fade show"></div>

    <!-- edit book modal -->
    <div ref="editBookModal" class="modal fade" :class="{ show: activeEditBookModal, 'd-block': activeEditBookModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleEditBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="editBookTitle" class="form-label">Title:</label>
                <input type="text" class="form-control" id="editBookTitle" v-model="editBookForm.title" placeholder="Enter title" />
              </div>
              <div class="mb-3">
                <label for="editBookAuthor" class="form-label">Author:</label>
                <input type="text" class="form-control" id="editBookAuthor" v-model="editBookForm.author" placeholder="Enter author" />
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="editBookRead" v-model="editBookForm.read" />
                <label class="form-check-label" for="editBookRead">Read?</label>
              </div>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary btn-sm" @click="handleEditSubmit">Submit</button>
                <button type="button" class="btn btn-danger btn-sm" @click="handleEditCancel">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditBookModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from "axios";
import Alert from "./Alert.vue";
import { ElMessage } from "element-plus";
export default {
  data() {
    return {
      activeAddBookModal: false,
      activeEditBookModal: false,
      fileList: [], // 添加文件列表数据
      trData: [],
      addBookForm: {
        title: "",
        author: "",
        read: [],
      },
      books: [],
      editBookForm: {
        id: "",
        title: "",
        author: "",
        read: [],
      },
      message: "",
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    // 上传成功处理
    handleSuccess(response) {
      ElMessage.success("文件上传成功");
      console.log("上传成功:", response.data);
    },

    // 上传失败处理
    handleError(error) {
      ElMessage.error("文件上传失败");
      console.error("上传失败:", error);
    },

    // 上传前验证
    beforeUpload(file) {
      const isExcel = file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || file.type === "application/vnd.ms-excel";
      if (!isExcel) {
        ElMessage.error("只能上传Excel文件!");
        return false;
      }

      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        ElMessage.error("文件大小不能超过 2MB!");
        return false;
      }
      return true;
    },

    // 超出限制处理
    handleExceed() {
      ElMessage.warning("每次只能上传一个文件");
    },
    addBook(payload) {
      const path = "http://localhost:5001/books";
      axios
        .post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = "Book added!";
          this.showMessage = true;
          ElMessage({
            message: "Congrats, this is a success message.",
            type: "success",
          });
        })
        .catch((error) => {
          console.log(error);
          this.getBooks();
        });
    },
    getTrCode() {
      const path = "http://localhost:5001/trCode";
      axios
        .get(path)
        .then((res) => {
          this.trData = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getBooks() {
      const path = "http://localhost:5001/books";
      axios
        .get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddBookModal();
      let read = false;
      if (this.addBookForm.read[0]) {
        read = true;
      }
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        read, // property shorthand
      };
      this.addBook(payload);
      this.initForm();
    },
    handleDeleteBook(book) {
      this.removeBook(book.id);
    },
    handleEditCancel() {
      this.toggleEditBookModal(null);
      this.initForm();
      this.getBooks(); // why?
    },
    handleEditSubmit() {
      this.toggleEditBookModal(null);
      let read = false;
      if (this.editBookForm.read) read = true;
      const payload = {
        title: this.editBookForm.title,
        author: this.editBookForm.author,
        read,
      };
      this.updateBook(payload, this.editBookForm.id);
    },
    initForm() {
      this.addBookForm.title = "";
      this.addBookForm.author = "";
      this.addBookForm.read = [];
      this.editBookForm.id = "";
      this.editBookForm.title = "";
      this.editBookForm.author = "";
      this.editBookForm.read = [];
    },
    removeBook(bookID) {
      const path = `http://localhost:5001/books/${bookID}`;
      axios
        .delete(path)
        .then(() => {
          this.getBooks();
          this.message = "Book removed!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getBooks();
        });
    },

    toggleEditBookModal(book) {
      if (book) {
        this.editBookForm = book;
      }
      const body = document.querySelector("body");
      this.activeEditBookModal = !this.activeEditBookModal;
      if (this.activeEditBookModal) {
        body.classList.add("modal-open");
      } else {
        body.classList.remove("modal-open");
      }
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5001/books/${bookID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = "Book updated!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getBooks();
        });
    },
  },
  created() {
    this.getTrCode();
  },
};
</script>
