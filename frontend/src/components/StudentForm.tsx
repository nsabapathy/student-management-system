import { useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import type { FormikProps } from 'formik';
import * as Yup from 'yup';
import api from '../utils/api';

interface StudentFormData {
  name: string;
  email: string;
  grade_level: string;
  description: string;
  age: number;
  address: string;
  role: string;
}

const initialValues: StudentFormData = {
  name: '',
  email: '',
  grade_level: '1',
  description: '',
  age: 5,
  address: '',
  role: 'student'
};

const validationSchema = Yup.object({
  name: Yup.string()
    .min(2, 'Must be at least 2 characters')
    .max(50, 'Must be 50 characters or less')
    .required('Required'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Required'),
  grade_level: Yup.string()
    .matches(/^[1-9]$|^1[0-2]$/, 'Must be a number between 1-12')
    .required('Required'),
  description: Yup.string()
    .max(500, 'Must be 500 characters or less'),
  age: Yup.number()
    .min(5, 'Must be at least 5')
    .max(17, 'Must be less than 18')
    .required('Required'),
  address: Yup.string()
    .min(10, 'Must be at least 10 characters')
    .max(200, 'Must be 200 characters or less')
    .required('Required'),
  role: Yup.string()
    .oneOf(['student', 'teacher'], 'Invalid role')
    .required('Required')
});

export default function StudentForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditing = Boolean(id);
  const formikRef = useRef<FormikProps<StudentFormData>>(null);

  useEffect(() => {      if (isEditing) {
        const fetchStudent = async () => {
          try {
            // Use our API client which automatically adds the auth token
            const response = await api.get(`/v1/students/${id}`);
          const student = response.data;
          
          // Implementation of form value setting with formik
          if (formikRef.current) {
            formikRef.current.setValues({
              name: student.name,
              email: student.email,
              grade_level: student.grade.toString(), // Convert numeric grade back to string
              description: student.description || '',
              age: student.age,
              address: student.address,
              role: student.role || 'student'
            });
          }
        } catch (error) {
          console.error('Failed to fetch student:', error);
          navigate('/v1/students/');
        }
      };
      fetchStudent();
    }
  }, [id, isEditing, navigate]);

  const handleSubmit = async (values: StudentFormData) => {
    try {
      // Transform data to match backend schema
      // Remove any fields that aren't expected by the backend
      const studentData = {
        name: values.name,
        email: values.email,
        grade: parseInt(values.grade_level), // Convert grade_level to numeric grade
        age: values.age,
        address: values.address,
        description: values.description || '',
      };
      
      console.log('Submitting student data:', studentData);
      
      if (isEditing) {
        const response = await api.put(`/v1/students/${id}`, studentData);
        console.log('Update response:', response.data);
      } else {
        const response = await api.post('/v1/students/', studentData);
        console.log('Create response:', response.data);
      }
      navigate('/v1/students/');
    } catch (error: any) {
      console.error('Failed to save student:', error);
      alert(`Failed to save student: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="px-4 py-6 sm:px-0">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">
          {isEditing ? 'Edit Student' : 'Add New Student'}
        </h1>
        <Formik
          innerRef={formikRef}
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ errors, touched }) => (
            <Form className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Name
                </label>
                <Field
                  name="name"
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.name && touched.name && (
                  <div className="text-red-500 text-sm mt-1">{errors.name}</div>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <Field
                  name="email"
                  type="email"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.email && touched.email && (
                  <div className="text-red-500 text-sm mt-1">{errors.email}</div>
                )}
              </div>

              <div>
                <label htmlFor="grade_level" className="block text-sm font-medium text-gray-700">
                  Grade Level (1-12)
                </label>
                <Field
                  name="grade_level"
                  type="number"
                  min="1"
                  max="12"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.grade_level && touched.grade_level && (
                  <div className="text-red-500 text-sm mt-1">{errors.grade_level}</div>
                )}
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <Field
                  name="description"
                  as="textarea"
                  rows={4}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.description && touched.description && (
                  <div className="text-red-500 text-sm mt-1">{errors.description}</div>
                )}
              </div>

              <div>
                <label htmlFor="age" className="block text-sm font-medium text-gray-700">
                  Age
                </label>
                <Field
                  name="age"
                  type="number"
                  min="5"
                  max="17"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.age && touched.age && (
                  <div className="text-red-500 text-sm mt-1">{errors.age}</div>
                )}
              </div>

              <div>
                <label htmlFor="address" className="block text-sm font-medium text-gray-700">
                  Address
                </label>
                <Field
                  name="address"
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.address && touched.address && (
                  <div className="text-red-500 text-sm mt-1">{errors.address}</div>
                )}
              </div>

              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700">
                  Role
                </label>
                <Field
                  name="role"
                  as="select"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="student">Student</option>
                  <option value="teacher">Teacher</option>
                </Field>
                {errors.role && touched.role && (
                  <div className="text-red-500 text-sm mt-1">{errors.role}</div>
                )}
              </div>

              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => navigate('/v1/students/')}
                  className="bg-gray-200 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  {isEditing ? 'Update' : 'Create'}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}
