import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../utils/api';

interface Student {
  _id: string;
  id: string;
  name: string;
  email: string;
  grade: number;
  grade_level?: string; // For compatibility with UI
  age: number;
  address: string;
  description?: string;
  role?: string;
}

export default function StudentList() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        console.log('Attempting to fetch students...');
        // Make API request (auth header is added by our api client)
        const response = await api.get('/v1/students/');
        
        console.log('API Response:', response);
        
        // Make sure we're getting an array from the response
        if (Array.isArray(response.data)) {
          // Transform the data to match our frontend structure
          const transformedData = response.data.map((student: any) => ({
            ...student,
            _id: student.id || student._id, // Use id or _id if available
            grade_level: student.grade?.toString() || student.grade_level // Use existing grade_level or convert grade
          }));
          setStudents(transformedData);
        } else if (response.data && Array.isArray(response.data.data)) {
          // Some APIs wrap the data in a data property
          const transformedData = response.data.data.map((student: any) => ({
            ...student,
            _id: student.id || student._id,
            grade_level: student.grade?.toString() || student.grade_level
          }));
          setStudents(transformedData);
        } else {
          console.error('Expected array but got:', response.data);
          setError('Received unexpected data format from server');
          setStudents([]);
        }
        setLoading(false);
      } catch (err: any) {
        console.error('API request failed:', err);
        
        // Check if it's an authentication error
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          // If unauthorized, clear token and redirect to login
          localStorage.removeItem('token');
          window.location.href = '/login';
          return;
        }
        
        setError('Failed to fetch students. Please make sure the API is running and accessible.');
        setStudents([]); // Ensure students is always an array
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this student?')) {
      try {
        // Use the server-expected ID format (from the 'id' field)
        const actualId = students.find(s => s._id === id)?.id || id;
        
        await api.delete(`/v1/students/${actualId}`);
        setStudents(students.filter(student => student._id !== id));
      } catch (err) {
        console.error('Delete failed:', err);
        setError('Failed to delete student');
      }
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-semibold text-gray-900">Students</h1>
          <Link
            to="/students/new"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Add New Student
          </Link>
        </div>
        <div className="flex flex-col">
          <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
              <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Name
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Email
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Grade Level
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Age
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Role
                      </th>
                      <th scope="col" className="relative px-6 py-3">
                        <span className="sr-only">Actions</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {students.map((student) => (
                      <tr key={student._id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {student.name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {student.email}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {student.grade_level}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {student.age}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {student.role}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <Link to={`/students/${student._id}/edit`} className="text-indigo-600 hover:text-indigo-900 mr-4">
                            Edit
                          </Link>
                          <button
                            onClick={() => handleDelete(student._id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
